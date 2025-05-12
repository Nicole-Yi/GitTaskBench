import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
from humor_quotes_spider import HumorQuotesSpider
import os

output_dir = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Scrapy_03"
os.makedirs(output_dir, exist_ok=True)

settings = get_project_settings()
settings.set("FEED_URI", os.path.join(output_dir, "output.xml"))
settings.set("FEED_FORMAT", "xml")

configure_logging()
runner = CrawlerRunner(settings)
runner.crawl(HumorQuotesSpider)
d = runner.join()
d.addBoth(lambda _: reactor.stop())

reactor.run()