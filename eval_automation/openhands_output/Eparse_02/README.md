# Excel Parser

This tool uses the Eparse library to parse Excel files and serialize the data into a text file in JSON format.

## Usage

### Using the Simple Script

```bash
python parse_excel.py
```

This script will parse the Excel file at `/data/data/agent_test_codebase/GitTaskBench/queries/Eparse_02/input/Eparse_02_input.xlsx` and save the serialized data to `/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Eparse_02/output.txt`.

### Using the CLI Script

```bash
python parse_excel_cli.py -i <input_excel_file> -o <output_text_file>
```

Example:
```bash
python parse_excel_cli.py -i /path/to/your/excel/file.xlsx -o /path/to/your/output/file.txt
```

## Output Format

The output is a JSON array of objects, where each object represents a cell in the Excel file with the following properties:

- `row`: The row index (0-based)
- `column`: The column index (0-based)
- `value`: The value of the cell
- `type`: The Python type of the value
- `c_header`: The column header
- `r_header`: The row header
- `excel_RC`: The Excel reference (e.g., "A1")
- `name`: The name of the table
- `sheet`: The name of the sheet
- `f_name`: The name of the Excel file

## Requirements

- Python 3.6+
- Eparse library
- pandas
- openpyxl

## Installation

```bash
pip install -e /path/to/Eparse
```