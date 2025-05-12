import requests
from bs4 import BeautifulSoup
import os

def fetch_url(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

def extract_main_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Simple content extraction logic
    main_content = soup.find('div', class_='main-content') or \
                   soup.find('article') or \
                   soup.find('div', role='main')
    
    if main_content:
        return '\n'.join(p.get_text() for p in main_content.find_all(['p', 'h1', 'h2', 'h3']))
    return None

url = "https://finance.sina.com.cn/zt_d/subject-1745887515/"
output_dir = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Trafilatura_02"
os.makedirs(output_dir, exist_ok=True)

html = fetch_url(url)
content = extract_main_content(html)

with open(f"{output_dir}/output.md", "w", encoding="utf-8") as f:
    f.write(content or "No content extracted")
print("Extraction completed")