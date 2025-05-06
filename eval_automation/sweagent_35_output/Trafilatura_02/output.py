import sys
import os

# Add Trafilatura to Python path
sys.path.append('/data/data/agent_test_codebase/GitTaskBench/code_base/Trafilatura')

import trafilatura

def main():
    # Read URL from input file
    input_file = '/data/data/agent_test_codebase/GitTaskBench/queries/Trafilatura_02/input/Trafilatura_02_input.txt'
    with open(input_file, 'r') as f:
        url = f.read().strip()

    # Download and extract content with timeout
    try:
        import requests
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        response = requests.get(url, timeout=5.0, headers=headers)
        response.raise_for_status()
        response.encoding = 'utf-8'  # Force UTF-8 encoding
        downloaded = response.text
    except Exception as e:
        print(f"Error downloading webpage: {e}")
        return

    # Extract content and convert to markdown
    try:
        # Convert bytes to string if needed
        if isinstance(downloaded, bytes):
            try:
                downloaded = downloaded.decode('utf-8')
            except UnicodeDecodeError:
                downloaded = downloaded.decode('gb18030')
        result = trafilatura.extract(downloaded, output_format='markdown', include_comments=False)
        if result is None:
            print("Error: Could not extract content from the webpage")
            return
    except Exception as e:
        print(f"Error extracting content: {e}")
        return

    # Save the result
    output_file = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Trafilatura_02/output.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"Content successfully extracted and saved to {output_file}")

if __name__ == '__main__':
    main()
