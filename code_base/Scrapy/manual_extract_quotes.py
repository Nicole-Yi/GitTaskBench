
import requests
from bs4 import BeautifulSoup
import json

base_url = "https://quotes.toscrape.com"
start_url = f"{base_url}/tag/humor/"

quotes_list = []
next_page = start_url

while next_page:
    response = requests.get(next_page)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for quote in soup.select('div.quote'):
        text = quote.select_one('span.text').get_text()
        author = quote.select_one('small.author').get_text()
        tags = [tag.get_text() for tag in quote.select('div.tags a.tag')]
        
        quotes_list.append({'text': text, 'author': author, 'tags': tags})

    next_button = soup.select_one('li.next a')
    next_page = f"{base_url}{next_button['href']}" if next_button else None

with open('/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Scrapy_01/output.json', 'w') as f:
    json.dump(quotes_list, f, ensure_ascii=False, indent=2)