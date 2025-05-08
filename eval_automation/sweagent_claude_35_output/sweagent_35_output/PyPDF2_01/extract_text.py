
import sys
import os
from pypdf import PdfReader

def extract_text_from_pdf(pdf_path, output_path):
    # Create reader object
    reader = PdfReader(pdf_path)
    
    # Get total number of pages
    number_of_pages = len(reader.pages)
    
    # Extract text from all pages
    text = ""
    for i in range(number_of_pages):
        page = reader.pages[i]
        text += page.extract_text()
        # Add a newline between pages
        if i < number_of_pages - 1:
            text += "\n\n"
    
    # Write text to output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

def main():
    # Input PDF path
    pdf_path = "/data/data/agent_test_codebase/GitTaskBench/queries/PyPDF2_01/input/PyPDF2_01_input.pdf"
    
    # Output text file path
    output_dir = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/PyPDF2_01"
    output_path = os.path.join(output_dir, "output.txt")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract text and save to file
    extract_text_from_pdf(pdf_path, output_path)
    print(f"Text has been extracted from {pdf_path} and saved to {output_path}")

if __name__ == "__main__":
    main()