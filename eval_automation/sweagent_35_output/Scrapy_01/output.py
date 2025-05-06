
import urllib.request
import json
import re
from html.parser import HTMLParser

class QuoteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.quotes = []
        self.current_quote = {'tags': []}
        self.capturing_text = False
        self.capturing_author = False
        self.capturing_tags = False
        
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'span' and 'class' in attrs and 'text' in attrs['class']:
            self.capturing_text = True
        elif tag == 'small' and 'class' in attrs and 'author' in attrs['class']:
            self.capturing_author = True
            self.current_quote['tags'] = []
        elif tag == 'a' and 'class' in attrs and 'tag' in attrs['class']:
            self.capturing_tags = True
            
    def handle_endtag(self, tag):
        if tag == 'span' and self.capturing_text:
            self.capturing_text = False
        elif tag == 'small' and self.capturing_author:
            self.capturing_author = False
        elif tag == 'a' and self.capturing_tags:
            self.capturing_tags = False
        elif tag == 'div' and self.current_quote:
            if 'text' in self.current_quote and 'author' in self.current_quote:
                self.quotes.append(self.current_quote.copy())
                self.current_quote = {'tags': []}
            
    def handle_data(self, data):
        if self.capturing_text:
            self.current_quote['text'] = data.strip().strip('"')
        elif self.capturing_author:
            self.current_quote['author'] = data.strip()
        elif self.capturing_tags:
            self.current_quote['tags'].append(data.strip())

def scrape_quotes(url):
    # Open URL and read content
    with urllib.request.urlopen(url) as response:
        html = response.read().decode('utf-8')
    
    # Parse quotes
    parser = QuoteParser()
    parser.feed(html)
    
    # Save to file
    output_path = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Scrapy_01/output.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(parser.quotes, f, ensure_ascii=False, indent=4)
    
    print(f"Scraped {len(parser.quotes)} quotes and saved to {output_path}")

if __name__ == '__main__':
    url = 'https://quotes.toscrape.com/tag/humor/'
    scrape_quotes(url)