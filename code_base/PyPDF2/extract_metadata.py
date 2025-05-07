
from pypdf import PdfReader

# Define the path to the input PDF and the output directory
input_pdf_path = '/data/data/agent_test_codebase/GitTaskBench/queries/PyPDF2_03/input/PyPDF2_03_input.pdf'
output_dir = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/PyPDF2_03/'

# Read the PDF file
reader = PdfReader(input_pdf_path)

# Get the metadata
meta = reader.metadata

# Prepare metadata for output
metadata_info = f"Title: {meta.title}\nAuthor: {meta.author}\nCreation Date: {meta.creation_date}\n"

# Define the output file path
output_file_path = output_dir + 'output.txt'

# Write the metadata to the output file
with open(output_file_path, 'w') as file:
    file.write(metadata_info)

print('Metadata extraction complete.')