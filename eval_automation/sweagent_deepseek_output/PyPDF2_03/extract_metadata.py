
import sys
sys.path.append("/data/data/agent_test_codebase/GitTaskBench/code_base/PyPDF2")
from pypdf import PdfReader

# Path to the input PDF file
input_pdf = "/data/data/agent_test_codebase/GitTaskBench/queries/PyPDF2_03/input/PyPDF2_03_input.pdf"

# Read the PDF file
reader = PdfReader(input_pdf)

# Extract metadata
meta = reader.metadata

# Save metadata to a file
output_file = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/PyPDF2_03/output.txt"
with open(output_file, "w") as f:
    f.write(f"Title: {meta.title}\n")
    f.write(f"Author: {meta.author}\n")
    f.write(f"Creation Date: {meta.creation_date}\n")