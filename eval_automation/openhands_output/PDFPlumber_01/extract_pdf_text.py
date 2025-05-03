#!/usr/bin/env python3
"""
Script to extract text from a PDF file using pdfplumber.
"""

import pdfplumber
import argparse
import os

def extract_pdf_text(pdf_path, output_path, page_num=0):
    """
    Extract text from a specific page of a PDF file and save it to a text file.
    
    Args:
        pdf_path (str): Path to the PDF file
        output_path (str): Path to save the extracted text
        page_num (int): Page number to extract (0-indexed, default is 0 for first page)
                        If -1, extract all pages
    """
    # Open the PDF file
    with pdfplumber.open(pdf_path) as pdf:
        # Check if the requested page exists
        if page_num >= len(pdf.pages) and page_num != -1:
            print(f"Error: The PDF only has {len(pdf.pages)} pages, but page {page_num+1} was requested.")
            return
        
        # Extract text from the specified page or all pages
        if page_num == -1:
            # Extract text from all pages
            text = ""
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                text += f"--- Page {i+1} ---\n{page_text}\n\n"
        else:
            # Extract text from the specified page
            page = pdf.pages[page_num]
            text = page.extract_text()
        
        # Write the extracted text to the output file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        if page_num == -1:
            print(f"Text extracted from all pages and saved to {output_path}")
        else:
            print(f"Text extracted from page {page_num+1} and saved to {output_path}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Extract text from a PDF file.')
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('--output', '-o', default='output.txt', help='Path to save the extracted text (default: output.txt)')
    parser.add_argument('--page', '-p', type=int, default=0, help='Page number to extract (0-indexed, default: 0 for first page, -1 for all pages)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Extract text from the PDF
    extract_pdf_text(args.pdf_path, args.output, args.page)