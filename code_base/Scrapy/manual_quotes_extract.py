
import requests
from bs4 import BeautifulSoup
import json

base_url = "https://quotes.toscrape.com/tag/humor/"
next_page = base_url
quotes = []

while next_page:
    response = requests.get(next_page)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        for quote in soup.select("div.quote"):
            text = quote.select_one("span.text").get_text(strip=True)
            author = quote.select_one("span small.author").get_text(strip=True)
            tags = [tag.get_text(strip=True) for tag in quote.select("div.tags a.tag")]
            quotes.append({"text": text, "author": author, "tags": tags})

        next_btn = soup.select_one("li.next a")
        next_page = base_url[:-1] + next_btn["href"] if next_btn else None
    else:
        break

with open("/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Scrapy_01/output.json", "w", encoding="utf-8") as f:
    json.dump(quotes, f, ensure_ascii=False, indent=2)