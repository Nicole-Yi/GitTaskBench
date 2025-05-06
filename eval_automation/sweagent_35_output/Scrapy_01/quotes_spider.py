
import scrapy
import json
import os

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['https://quotes.toscrape.com/tag/humor/']
    
    def parse(self, response):
        quotes = []
        for quote in response.css('div.quote'):
            quotes.append({
                'text': quote.css('span.text::text').get().strip('\"'),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall()
            })
            
        # Save to output file
        output_path = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Scrapy_01/output.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(quotes, f, ensure_ascii=False, indent=4)
            
        # Follow next page if it exists
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings
    
    # Add PYTHONPATH
    import sys
    sys.path.append('/data/data/agent_test_codebase/GitTaskBench/code_base/Scrapy')
    
    # Create and configure the crawler process
    process = CrawlerProcess(settings={
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    })
    
    # Start the crawling process
    process.crawl(QuotesSpider)
    process.start()