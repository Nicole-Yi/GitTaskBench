#!/usr/bin/env python3
"""
Script to extract text from a PDF file and save it to a text file using PyPDF2.
"""

import os
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path, output_path):
    """
    Extract text from a PDF file and save it to a text file.
    
    Args:
        pdf_path (str): Path to the PDF file
        output_path (str): Path to save the extracted text
    """
    # Create a PDF reader object
    reader = PdfReader(pdf_path)
    
    # Get the number of pages in the PDF
    num_pages = len(reader.pages)
    print(f"PDF has {num_pages} pages")
    
    # Extract text from each page and concatenate
    all_text = ""
    for page_num in range(num_pages):
        page = reader.pages[page_num]
        text = page.extract_text()
        all_text += text + "\n\n"  # Add extra newlines between pages
    
    # Write the extracted text to a file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(all_text)
    
    print(f"Text extracted successfully and saved to {output_path}")

if __name__ == "__main__":
    # Define input and output paths
    pdf_path = "/data/data/agent_test_codebase/GitTaskBench/queries/PyPDF2_01/input/PyPDF2_01_input.pdf"
    output_path = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/PyPDF2_01/output.txt"
    
    # Extract text from PDF and save to text file
    extract_text_from_pdf(pdf_path, output_path)