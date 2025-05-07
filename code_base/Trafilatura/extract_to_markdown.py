
import trafilatura

# Load the URL from the input file
with open('/data/data/agent_test_codebase/GitTaskBench/queries/Trafilatura_02/input/Trafilatura_02_input.txt', 'r') as file:
    url = file.readline().strip()

# Fetch and extract content from the URL
result = trafilatura.fetch_url(url)
extracted = trafilatura.extract(result, output_format='md')

# Define the output directory and file path
output_dir = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Trafilatura_02'
output_file_path = f'{output_dir}/output.md'

# Save the markdown content to the output file
with open(output_file_path, 'w') as output_file:
    output_file.write(extracted)

print('Content extraction and conversion to markdown completed.')