
from trafilatura.trafilatura import fetch_url, extract

# Define paths
input_file = '/data/data/agent_test_codebase/GitTaskBench/queries/Trafilatura_01/input/Trafilatura_01_input.txt'
output_file = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Trafilatura_01/output.txt'

# Read the URL from the input file
with open(input_file, 'r') as file:
    url = file.read().strip()

# Fetch and extract content using Trafilatura
downloaded = fetch_url(url)
result = extract(downloaded)

# Save the result to the output file
with open(output_file, 'w') as file:
    file.write(result)
    
print('Extraction completed successfully.')