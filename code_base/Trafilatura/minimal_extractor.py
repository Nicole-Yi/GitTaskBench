import requests
from bs4 import BeautifulSoup
import sys

url = "https://www.cnprose.com/article-detail/WJaljpMN"
output_file = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Trafilatura_03/output.txt"
timeout = 15  # seconds

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

try:
    print(f"Attempting to fetch {url} with {timeout}s timeout and browser headers...")
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    
    print("Parsing HTML content...")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract metadata
    metadata = {
        'title': soup.title.string if soup.title else 'N/A',
        'description': soup.find('meta', attrs={'name': 'description'})['content'] 
                      if soup.find('meta', attrs={'name': 'description'}) else 'N/A',
        'url': url
    }
    
    print("Writing results...")
    with open(output_file, 'w', encoding='utf-8') as f:
        for key, value in metadata.items():
            f.write(f"{key.capitalize()}: {value}\n")
    
    print(f"Successfully saved metadata to {output_file}")
    print("Extracted metadata:")
    for key, value in metadata.items():
        print(f"{key.capitalize()}: {value}")
        
except requests.exceptions.Timeout:
    print(f"Error: Request timed out after {timeout} seconds", file=sys.stderr)
except Exception as e:
    print(f"Error: {str(e)}", file=sys.stderr)
    sys.exit(1)