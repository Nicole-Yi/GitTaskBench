from scrapy.crawler import CrawlerProcess
from humor_quotes_spider import HumorQuotesSpider
import os

output_dir = "../eval_automation/output/Scrapy_03"
os.makedirs(output_dir, exist_ok=True)

process = CrawlerProcess(settings={
    "FEEDS": {
        f"{output_dir}/output.xml": {"format": "xml"}
    }
})
process.crawl(HumorQuotesSpider)
process.start()