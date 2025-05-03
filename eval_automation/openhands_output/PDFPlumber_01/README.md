# PDF Text Extraction

This repository contains scripts to extract text from PDF files using the PDFPlumber library.

## Requirements

- Python 3.x
- pdfplumber library (`pip install pdfplumber`)

## Scripts

### 1. extract_text.py

This script is specifically configured to extract text from the first page of the specified input PDF file.

#### Usage

```
python extract_text.py
```

The script is configured to:
- Extract text from: `/data/data/agent_test_codebase/GitTaskBench/queries/PDFPlumber_01/input/PDFPlumber_01_input.pdf`
- Save the extracted text to: `/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/PDFPlumber_01/output.txt`

### 2. extract_pdf_text.py

This is a more flexible script that can extract text from any page of any PDF file.

#### Usage

```
python extract_pdf_text.py path/to/pdf_file.pdf [options]
```

#### Options

- `--output`, `-o`: Path to save the extracted text (default: output.txt)
- `--page`, `-p`: Page number to extract (0-indexed, default: 0 for first page, -1 for all pages)

#### Examples

Extract the first page of a PDF:
```
python extract_pdf_text.py input.pdf -o output.txt
```

Extract the second page of a PDF:
```
python extract_pdf_text.py input.pdf -o output.txt -p 1
```

Extract all pages of a PDF:
```
python extract_pdf_text.py input.pdf -o output.txt -p -1
```

## How it works

The scripts use pdfplumber to:
1. Open the PDF file
2. Access the specified page(s)
3. Extract all text content using the `extract_text()` method
4. Save the extracted text to a text file