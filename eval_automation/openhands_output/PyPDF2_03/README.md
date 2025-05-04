# PDF Metadata Extraction

This directory contains a script and output files for extracting metadata from PDF files using the PyPDF2 library.

## Files

- `extract_metadata.py`: Python script to extract metadata from PDF files
- `output.json`: Extracted metadata in JSON format
- `output.txt`: Extracted metadata in human-readable text format

## How to Use

To extract metadata from a different PDF file, you can modify the `input_pdf` variable in the `extract_metadata.py` script and run it:

```bash
python extract_metadata.py
```

## Metadata Extracted

The script extracts the following metadata from PDF files:

- Title
- Author
- Subject
- Creator
- Producer
- Creation Date
- Modification Date
- Number of Pages

## Requirements

- Python 3.x
- PyPDF2 library (install with `pip install pypdf`)

## Example Usage in Code

```python
from pypdf import PdfReader

# Open the PDF file
reader = PdfReader("path/to/your/file.pdf")

# Access metadata
meta = reader.metadata

# Print metadata
print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
print(f"Subject: {meta.subject}")
print(f"Creator: {meta.creator}")
print(f"Producer: {meta.producer}")
print(f"Creation Date: {meta.creation_date}")
print(f"Modification Date: {meta.modification_date}")
print(f"Number of Pages: {len(reader.pages)}")
```