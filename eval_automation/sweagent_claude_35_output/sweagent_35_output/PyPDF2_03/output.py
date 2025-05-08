
import sys
sys.path.append('/data/data/agent_test_codebase/GitTaskBench/code_base/PyPDF2')

from pypdf import PdfReader

# Input PDF file path
pdf_path = "/data/data/agent_test_codebase/GitTaskBench/queries/PyPDF2_03/input/PyPDF2_03_input.pdf"

# Create a PDF reader object
reader = PdfReader(pdf_path)

# Get metadata
meta = reader.metadata

# Print all metadata
print("PDF Metadata:")
print("-" * 50)
print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
print(f"Creator: {meta.creator}")
print(f"Producer: {meta.producer}")
print(f"Creation Date: {meta.creation_date}")
print(f"Modification Date: {meta.modification_date}")
print(f"Subject: {meta.subject}")
print("-" * 50)