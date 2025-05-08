#!/usr/bin/env python3
"""
Script to extract text from the first page of a PDF file using pdfplumber.
"""

import pdfplumber
import os

def extract_first_page_text(pdf_path, output_path):
    """
    Extract text from the first page of a PDF file and save it to a text file.
    
    Args:
        pdf_path (str): Path to the PDF file
        output_path (str): Path to save the extracted text
    """
    # Open the PDF file
    with pdfplumber.open(pdf_path) as pdf:
        # Get the first page
        first_page = pdf.pages[0]
        
        # Extract text from the first page
        text = first_page.extract_text()
        
        # Write the extracted text to the output file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"Text extracted from the first page and saved to {output_path}")

if __name__ == "__main__":
    # Define input and output paths
    pdf_path = "/data/data/agent_test_codebase/GitTaskBench/queries/PDFPlumber_01/input/PDFPlumber_01_input.pdf"
    output_path = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/PDFPlumber_01/output.txt"
    
    # Extract text from the first page
    extract_first_page_text(pdf_path, output_path)