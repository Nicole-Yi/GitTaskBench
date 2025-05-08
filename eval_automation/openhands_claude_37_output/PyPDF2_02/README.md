# PDF Splitter

This script splits a PDF file into individual pages, creating a separate PDF file for each page of the original document.

## Requirements

- Python 3.x
- PyPDF2 library

## Usage

The script can be run directly with Python:

```bash
python split_pdf.py
```

By default, the script:
1. Reads the input PDF from `/data/data/agent_test_codebase/GitTaskBench/queries/PyPDF2_02/input/PyPDF2_02_input.pdf`
2. Creates individual PDF files in the `/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/PyPDF2_02/` directory
3. Names the output files as `output_01.pdf`, `output_02.pdf`, etc.

## Customization

To use the script with different input and output paths, modify the following variables in the script:

```python
input_pdf = "/path/to/your/input.pdf"
output_directory = "/path/to/your/output/directory"
```

## How It Works

The script uses PyPDF2's PdfReader to read the input PDF and PdfWriter to create new PDFs for each page. For each page in the original PDF:

1. A new PdfWriter instance is created
2. The page is added to the writer
3. The writer saves the page as a new PDF file