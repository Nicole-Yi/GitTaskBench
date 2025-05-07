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
        import xml.etree.ElementTree as ET

        root = ET.Element('quotes')
        
        for quote in self.quotes_list:
            quote_elem = ET.SubElement(root, 'quote')
            text_elem = ET.SubElement(quote_elem, 'text')
            text_elem.text = quote['text']
            author_elem = ET.SubElement(quote_elem, 'author')
            author_elem.text = quote['author']
        
        output_path = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Scrapy_03/output.xml'
        tree = ET.ElementTree(root)
        tree.write(output_path, encoding='utf-8', xml_declaration=True)

