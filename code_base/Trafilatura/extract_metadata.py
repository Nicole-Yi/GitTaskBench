import sys
sys.path.append('/data/data/agent_test_codebase/GitTaskBench/code_base/Trafilatura')
from trafilatura.core import fetch_url
from trafilatura.metadata import extract_metadata

url = "https://www.cnprose.com/article-detail/WJaljpMN"
output_file = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Trafilatura_03/output.txt"

try:
    downloaded = fetch_url(url)
    metadata = extract_metadata(downloaded)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Title: {metadata.get('title', 'N/A')}\n")
        f.write(f"Author: {metadata.get('author', 'N/A')}\n")
        f.write(f"Date: {metadata.get('date', 'N/A')}\n")
        f.write(f"URL: {url}\n")
        
    print(f"Minimal metadata saved to {output_file}")
except Exception as e:
    print(f"Error: {str(e)}")