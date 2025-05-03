#!/usr/bin/env python3
"""
Script to split a PDF file into individual pages using PyPDF2.
Each page of the input PDF will be saved as a separate PDF file.
"""

import os
import sys
from pathlib import Path

# Add the PyPDF2 library to the Python path
sys.path.append('/data/data/agent_test_codebase/GitTaskBench/code_base/PyPDF2')

from pypdf import PdfReader, PdfWriter

def split_pdf(input_path, output_dir):
    """
    Split a PDF file into individual pages.
    
    Args:
        input_path (str): Path to the input PDF file
        output_dir (str): Directory where the output PDF files will be saved
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Read the input PDF
    reader = PdfReader(input_path)
    total_pages = len(reader.pages)
    
    print(f"Splitting PDF with {total_pages} pages...")
    
    # For each page, create a new PDF file
    for page_num in range(total_pages):
        # Create a PDF writer
        writer = PdfWriter()
        
        # Add the current page to the writer
        writer.add_page(reader.pages[page_num])
        
        # Create output filename with leading zeros for proper sorting
        output_filename = f"output_{page_num+1:02d}.pdf"
        output_path = os.path.join(output_dir, output_filename)
        
        # Write the page to a new PDF file
        with open(output_path, "wb") as output_file:
            writer.write(output_file)
        
        print(f"Created: {output_path}")
    
    print(f"Successfully split {total_pages} pages into individual PDF files.")

if __name__ == "__main__":
    # Define input and output paths
    input_pdf = "/data/data/agent_test_codebase/GitTaskBench/queries/PyPDF2_02/input/PyPDF2_02_input.pdf"
    output_directory = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/PyPDF2_02"
    
    # Split the PDF
    split_pdf(input_pdf, output_directory)