import sys
sys.path.insert(0, '/data/data/agent_test_codebase/GitTaskBench/code_base/PDFPlumber')
import pdfplumber

# Define input and output paths
input_pdf_path = "/data/data/agent_test_codebase/GitTaskBench/queries/PDFPlumber_01/input/PDFPlumber_01_input.pdf"
output_txt_path = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/PDFPlumber_01/output.txt"

# Open the PDF file
with pdfplumber.open(input_pdf_path) as pdf:
    # Get the first page
    page = pdf.pages[0]
    # Extract text from the first page
    text = page.extract_text()
    
# Write the extracted text to a file
with open(output_txt_path, "w") as txt_file:
    # Ensure that text is written to file only if text is not None
    if text:
        txt_file.write(text)