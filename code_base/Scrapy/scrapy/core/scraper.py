"""This module implements the Scraper component which parses responses and
extracts information from them"""

from __future__ import annotations

import logging
from collections import deque
from collections.abc import AsyncIterable, Iterator
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from twisted.internet.defer import Deferred, inlineCallbacks
from twisted.python.failure import Failure

from scrapy import Spider, signals
from scrapy.core.spidermw import SpiderMiddlewareManager
from scrapy.exceptions import CloseSpider, DropItem, IgnoreRequest
from scrapy.http import Request, Response
from scrapy.utils.defer import (
    aiter_errback,
    defer_fail,
    defer_succeed,
    iter_errback,
    parallel,
    parallel_async,
)
from scrapy.utils.log import failure_to_exc_info, logformatter_adapter
from scrapy.utils.misc import load_object, warn_on_generator_with_return_value
from scrapy.utils.spider import iterate_spider_output

if TYPE_CHECKING:
    from collections.abc import Generator, Iterable

    from scrapy.crawler import Crawler
    from scrapy.logformatter import LogFormatter
    from scrapy.pipelines import ItemPipelineManager
    from scrapy.signalmanager import SignalManager


logger = logging.getLogger(__name__)


_T = TypeVar("_T")
_ParallelResult = list[tuple[bool, Iterator[Any]]]
_HandleOutputDeferred = Deferred[Union[_ParallelResult, None]]
QueueTuple = tuple[Union[Response, Failure], Request, _HandleOutputDeferred]


class Slot:
    """Scraper slot (one per running spider)"""

    MIN_RESPONSE_SIZE = 1024

    def __init__(self, max_active_size: int = 5000000):
        self.max_active_size: int = max_active_size
        self.queue: deque[QueueTuple] = deque()
        self.active: set[Request] = set()
        self.active_size: int = 0
        self.itemproc_size: int = 0
        self.closing: Deferred[Spider] | None = None

    def add_response_request(
        self, result: Response | Failure, request: Request
    ) -> _HandleOutputDeferred:
        deferred: _HandleOutputDeferred = Deferred()
        self.queue.append((result, request, deferred))
        if isinstance(result, Response):
            self.active_size += max(len(result.body), self.MIN_RESPONSE_SIZE)
        else:
            self.active_size += self.MIN_RESPONSE_SIZE
        return deferred

    def next_response_request_deferred(self) -> QueueTuple:
        response, request, deferred = self.queue.popleft()
        self.active.add(request)
        return response, request, deferred

    def finish_response(self, result: Response | Failure, request: Request) -> None:
        self.active.remove(request)
        if isinstance(result, Response):
            self.active_size -= max(len(result.body), self.MIN_RESPONSE_SIZE)
        else:
            self.active_size -= self.MIN_RESPONSE_SIZE

    def is_idle(self) -> bool:
        return not (self.queue or self.active)

    def needs_backout(self) -> bool:
        return self.active_size > self.max_active_size


class Scraper:
    def __init__(self, crawler: Crawler) -> None:
        self.slot: Slot | None = None
        self.spidermw: SpiderMiddlewareManager = SpiderMiddlewareManager.from_crawler(
            crawler
        )
        itemproc_cls: type[ItemPipelineManager] = load_object(
            crawler.settings["ITEM_PROCESSOR"]
        )
        self.itemproc: ItemPipelineManager = itemproc_cls.from_crawler(crawler)
        self.concurrent_items: int = crawler.settings.getint("CONCURRENT_ITEMS")
        self.crawler: Crawler = crawler
        self.signals: SignalManager = crawler.signals
        assert crawler.logformatter
        self.logformatter: LogFormatter = crawler.logformatter

    @inlineCallbacks
    def open_spider(self, spider: Spider) -> Generator[Deferred[Any], Any, None]:
        """Open the given spider for scraping and allocate resources for it"""
        self.slot = Slot(self.crawler.settings.getint("SCRAPER_SLOT_MAX_ACTIVE_SIZE"))
        yield self.itemproc.open_spider(spider)

    def close_spider(self, spider: Spider) -> Deferred[Spider]:
        """Close a spider being scraped and release its resources"""
        if self.slot is None:
            raise RuntimeError("Scraper slot not assigned")
        self.slot.closing = Deferred()
        self.slot.closing.addCallback(self.itemproc.close_spider)
        self._check_if_closing(spider)
        return self.slot.closing

    def is_idle(self) -> bool:
        """Return True if there isn't any more spiders to process"""
        return not self.slot

    def _check_if_closing(self, spider: Spider) -> None:
        assert self.slot is not None  # typing
        if self.slot.closing and self.slot.is_idle():
            self.slot.closing.callback(spider)

    def enqueue_scrape(
        self, result: Response | Failure, request: Request, spider: Spider
    ) -> _HandleOutputDeferred:
        if self.slot is None:
            raise RuntimeError("Scraper slot not assigned")
        dfd = self.slot.add_response_request(result, request)

        def finish_scraping(_: _T) -> _T:
            assert self.slot is not None
            self.slot.finish_response(result, request)
            self._check_if_closing(spider)
            self._scrape_next(spider)
            return _

        dfd.addBoth(finish_scraping)
        dfd.addErrback(
            lambda f: logger.error(
                "Scraper bug processing %(request)s",
                {"request": request},
                exc_info=failure_to_exc_info(f),
                extra={"spider": spider},
            )
        )
        self._scrape_next(spider)
        return dfd

    def _scrape_next(self, spider: Spider) -> None:
        assert self.slot is not None  # typing
        while self.slot.queue:
            response, request, deferred = self.slot.next_response_request_deferred()
            self._scrape(response, request, spider).chainDeferred(deferred)

    def _scrape(
        self, result: Response | Failure, request: Request, spider: Spider
    ) -> _HandleOutputDeferred:
        """
        Handle the downloaded response or failure through the spider callback/errback
        """
        if not isinstance(result, (Response, Failure)):
            raise TypeError(
                f"Incorrect type: expected Response or Failure, got {type(result)}: {result!r}"
            )
        dfd: Deferred[Iterable[Any] | AsyncIterable[Any]] = self._scrape2(
            result, request, spider
        )  # returns spider's processed output
        dfd.addErrback(self.handle_spider_error, request, result, spider)
        dfd2: _HandleOutputDeferred = dfd.addCallback(
            self.handle_spider_output, request, cast(Response, result), spider
        )
        return dfd2

    def _scrape2(
        self, result: Response | Failure, request: Request, spider: Spider
    ) -> Deferred[Iterable[Any] | AsyncIterable[Any]]:
        """
        Handle the different cases of request's result been a Response or a Failure
        """
        if isinstance(result, Response):
            # Deferreds are invariant so Mutable*Chain isn't matched to *Iterable
            return self.spidermw.scrape_response(  # type: ignore[return-value]
                self.call_spider, result, request, spider
            )
        # else result is a Failure
        dfd = self.call_spider(result, request, spider)
        dfd.addErrback(self._log_download_errors, result, request, spider)
        return dfd

    def call_spider(
        self, result: Response | Failure, request: Request, spider: Spider
    ) -> Deferred[Iterable[Any] | AsyncIterable[Any]]:
        dfd: Deferred[Any]
        if isinstance(result, Response):
            if getattr(result, "request", None) is None:
                result.request = request
            assert result.request
            callback = result.request.callback or spider._parse
            warn_on_generator_with_return_value(spider, callback)
            dfd = defer_succeed(result)
            dfd.addCallbacks(
                callback=callback, callbackKeywords=result.request.cb_kwargs
            )
        else:  # result is a Failure
            # TODO: properly type adding this attribute to a Failure
            result.request = request  # type: ignore[attr-defined]
            dfd = defer_fail(result)
            if request.errback:
                warn_on_generator_with_return_value(spider, request.errback)
                dfd.addErrback(request.errback)
        dfd2: Deferred[Iterable[Any] | AsyncIterable[Any]] = dfd.addCallback(
            iterate_spider_output
        )
        return dfd2

    def handle_spider_error(
        self,
        _failure: Failure,
        request: Request,
        response: Response | Failure,
        spider: Spider,
    ) -> None:
        exc = _failure.value
        if isinstance(exc, CloseSpider):
            assert self.crawler.engine is not None  # typing
            self.crawler.engine.close_spider(spider, exc.reason or "cancelled")
            return
        logkws = self.logformatter.spider_error(_failure, request, response, spider)
        logger.log(
            *logformatter_adapter(logkws),
            exc_info=failure_to_exc_info(_failure),
            extra={"spider": spider},
        )
        self.signals.send_catch_log(
            signal=signals.spider_error,
            failure=_failure,
            response=response,
            spider=spider,
        )
        assert self.crawler.stats
        self.crawler.stats.inc_value("spider_exceptions/count", spider=spider)
        self.crawler.stats.inc_value(
            f"spider_exceptions/{_failure.value.__class__.__name__}", spider=spider
        )

    def handle_spider_output(
        self,
        result: Iterable[_T] | AsyncIterable[_T],
        request: Request,
        response: Response,
        spider: Spider,
    ) -> _HandleOutputDeferred:
        if not result:
            return defer_succeed(None)
        it: Iterable[_T] | AsyncIterable[_T]
        dfd: Deferred[_ParallelResult]
        if isinstance(result, AsyncIterable):
            it = aiter_errback(
                result, self.handle_spider_error, request, response, spider
            )
            dfd = parallel_async(
                it,
                self.concurrent_items,
                self._process_spidermw_output,
                request,
                response,
                spider,
            )
        else:
            it = iter_errback(
                result, self.handle_spider_error, request, response, spider
            )
            dfd = parallel(
                it,
                self.concurrent_items,
                self._process_spidermw_output,
                request,
                response,
                spider,
            )
        # returning Deferred[_ParallelResult] instead of Deferred[Union[_ParallelResult, None]]
        return dfd  # type: ignore[return-value]

    def _process_spidermw_output(
        self, output: Any, request: Request, response: Response, spider: Spider
    ) -> Deferred[Any] | None:
        """Process each Request/Item (given in the output parameter) returned
        from the given spider
        """
        if isinstance(output, Request):
            assert self.crawler.engine is not None  # typing
            self.crawler.engine.crawl(request=output)
        elif output is None:
            pass
        else:
            return self.start_itemproc(output, response=response)
        return None

    def start_itemproc(self, item: Any, *, response: Response | None) -> Deferred[Any]:
        """Send *item* to the item pipelines for processing.

        *response* is the source of the item data. If the item does not come
        from response data, e.g. it was hard-coded, set it to ``None``.
        """
        assert self.slot is not None  # typing
        assert self.crawler.spider is not None  # typing
        self.slot.itemproc_size += 1
        dfd = self.itemproc.process_item(item, self.crawler.spider)
        dfd.addBoth(self._itemproc_finished, item, response, self.crawler.spider)
        return dfd

    def _log_download_errors(
        self,
        spider_failure: Failure,
        download_failure: Failure,
        request: Request,
        spider: Spider,
    ) -> Failure | None:
        """Log and silence errors that come from the engine (typically download
        errors that got propagated thru here).

        spider_failure: the value passed into the errback of self.call_spider()
        download_failure: the value passed into _scrape2() from
        ExecutionEngine._handle_downloader_output() as "result"
        """
        if not download_failure.check(IgnoreRequest):
            if download_failure.frames:
                logkws = self.logformatter.download_error(
                    download_failure, request, spider
                )
                logger.log(
                    *logformatter_adapter(logkws),
                    extra={"spider": spider},
                    exc_info=failure_to_exc_info(download_failure),
                )
            else:
                errmsg = download_failure.getErrorMessage()
                if errmsg:
                    logkws = self.logformatter.download_error(
                        download_failure, request, spider, errmsg
                    )
                    logger.log(
                        *logformatter_adapter(logkws),
                        extra={"spider": spider},
                    )

        if spider_failure is not download_failure:
            return spider_failure
        return None

    def _itemproc_finished(
        self, output: Any, item: Any, response: Response | None, spider: Spider
    ) -> Deferred[Any]:
        """ItemProcessor finished for the given ``item`` and returned ``output``"""
        assert self.slot is not None  # typing
        self.slot.itemproc_size -= 1
        if isinstance(output, Failure):
            ex = output.value
            if isinstance(ex, DropItem):
                logkws = self.logformatter.dropped(item, ex, response, spider)
                if logkws is not None:
                    logger.log(*logformatter_adapter(logkws), extra={"spider": spider})
                return self.signals.send_catch_log_deferred(
                    signal=signals.item_dropped,
                    item=item,
                    response=response,
                    spider=spider,
                    exception=output.value,
                )
            assert ex
            logkws = self.logformatter.item_error(item, ex, response, spider)
            logger.log(
                *logformatter_adapter(logkws),
                extra={"spider": spider},
                exc_info=failure_to_exc_info(output),
            )
            return self.signals.send_catch_log_deferred(
                signal=signals.item_error,
                item=item,
                response=response,
                spider=spider,
                failure=output,
            )
        logkws = self.logformatter.scraped(output, response, spider)
        if logkws is not None:
            logger.log(*logformatter_adapter(logkws), extra={"spider": spider})
        return self.signals.send_catch_log_deferred(
            signal=signals.item_scraped, item=output, response=response, spider=spider
        )
