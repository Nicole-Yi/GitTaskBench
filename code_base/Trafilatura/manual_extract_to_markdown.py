
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify

# Define paths 
input_file_path = '/data/data/agent_test_codebase/GitTaskBench/queries/Trafilatura_02/input/Trafilatura_02_input.txt'
output_dir = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Trafilatura_02'

# Load URL from input file
with open(input_file_path, 'r') as file:
    url = file.readline().strip()

# Fetch the webpage content
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Convert HTML to markdown format
markdown_content = markdownify(str(soup))

# Define output file path
output_file_path = f'{output_dir}/output.md'

# Save the markdown content to a file
with open(output_file_path, 'w') as output_file:
    output_file.write(markdown_content)

print('Content extracted and saved in markdown format successfully.')