
import os
import sys
import json
import urllib.request
from html.parser import HTMLParser
from datetime import datetime

class MetadataParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.description = ""
        self.author = ""
        self.text = []
        self.in_title = False
        self.in_p = False

    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.in_title = True
        elif tag == 'meta':
            attrs_dict = dict(attrs)
            if attrs_dict.get('name') == 'description':
                self.description = attrs_dict.get('content', '')
            elif attrs_dict.get('name') == 'author':
                self.author = attrs_dict.get('content', '')
        elif tag == 'p':
            self.in_p = True

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        elif tag == 'p':
            self.in_p = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        elif self.in_p:
            self.text.append(data.strip())

# Read the URL from input file
with open('/data/data/agent_test_codebase/GitTaskBench/queries/Trafilatura_03/input/Trafilatura_03_input.txt', 'r') as f:
    url = f.read().strip()

# Ensure the output directory exists
output_dir = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Trafilatura_03'
output_file = os.path.join(output_dir, 'output.txt')
os.makedirs(output_dir, exist_ok=True)

try:
    # Download webpage
    response = urllib.request.urlopen(url)
    html_content = response.read().decode('utf-8')

    # Parse HTML and extract metadata
    parser = MetadataParser()
    parser.feed(html_content)

    # Combine metadata
    metadata = {
        'url': url,
        'title': parser.title,
        'description': parser.description,
        'author': parser.author,
        'sitename': 'cnprose.com',
        'date': datetime.now().isoformat(),
        'text': '\n'.join(parser.text)
    }

    # Save as JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print(f"Content has been extracted and saved to {output_file}")

except Exception as e:
    print(f"Error: {e}")
    exit(1)