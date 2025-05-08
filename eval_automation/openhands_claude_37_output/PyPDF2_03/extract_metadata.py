#!/usr/bin/env python3
"""
Extract metadata from a PDF file using PyPDF2 library.
"""

import json
import os
from datetime import datetime
from pypdf import PdfReader

def extract_pdf_metadata(pdf_path):
    """
    Extract metadata from a PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        dict: Dictionary containing the metadata
    """
    reader = PdfReader(pdf_path)
    meta = reader.metadata
    
    # Create a dictionary to store the metadata
    metadata = {
        "title": meta.title,
        "author": meta.author,
        "subject": meta.subject,
        "creator": meta.creator,
        "producer": meta.producer,
        "creation_date": None,
        "modification_date": None
    }
    
    # Handle date objects (they might be None)
    if meta.creation_date:
        metadata["creation_date"] = str(meta.creation_date)
    
    if meta.modification_date:
        metadata["modification_date"] = str(meta.modification_date)
    
    # Add number of pages
    metadata["number_of_pages"] = len(reader.pages)
    
    return metadata

def main():
    # Input and output paths
    input_pdf = "/data/data/agent_test_codebase/GitTaskBench/queries/PyPDF2_03/input/PyPDF2_03_input.pdf"
    output_dir = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/PyPDF2_03"
    output_file = os.path.join(output_dir, "output.json")
    
    # Extract metadata
    metadata = extract_pdf_metadata(input_pdf)
    
    # Save metadata to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)
    
    print(f"Metadata extracted and saved to {output_file}")
    
    # Also print the metadata to console
    print("\nExtracted Metadata:")
    for key, value in metadata.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()