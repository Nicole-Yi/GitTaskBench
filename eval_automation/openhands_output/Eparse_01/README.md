# Excel Sheet Scanner

This script scans all Excel files in a specified directory, extracts their sheet information, and saves it to a text file.

## Features

- Finds all Excel files (`.xlsx`, `.xls`, `.xlsm`) in a directory
- Extracts sheet names and dimensions
- Shows sample data (headers) from each sheet
- Provides detailed information using pandas (rows, columns, data types)
- Saves all information to a text file

## Usage

```bash
python excel_sheet_scanner.py <directory_path> <output_file>
```

### Arguments

- `directory_path`: Path to the directory containing Excel files
- `output_file`: Path to the output text file

### Example

```bash
python excel_sheet_scanner.py /path/to/excel/files /path/to/output.txt
```

## Output Format

The output file contains the following information for each Excel file:

1. File name
2. Sheet names
3. Number of rows and columns in each sheet
4. Sample data (headers) from each sheet
5. Additional information from pandas, such as column names, data types, and empty cells

## Requirements

- Python 3.6+
- openpyxl
- pandas

## Installation

```bash
pip install openpyxl pandas
```