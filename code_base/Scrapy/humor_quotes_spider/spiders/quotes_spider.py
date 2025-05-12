import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://quotes.toscrape.com/tag/humor/',
    ]

    def parse(self, response):
        self.quotes_list = []
        
        for quote in response.css('div.quote'):
            self.quotes_list.append({
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
            })

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def close(self, reason):
        import csv

        output_path = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Scrapy_02/output.csv'
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['author', 'text']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for quote in self.quotes_list:
                writer.writerow(quote)

