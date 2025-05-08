# Excel to JSON Converter

This directory contains scripts to convert Excel files to JSON format using the Eparse library.

## Files

- `excel_to_json.py`: Converts Excel file to a flat JSON array where each element represents a cell in the Excel file.
- `excel_to_structured_json.py`: Converts Excel file to a structured JSON object that groups data by sheets and tables.
- `output.json`: The flat JSON output.
- `output_structured.json`: The structured JSON output.

## Usage

### Flat JSON Conversion

```bash
python excel_to_json.py
```

This script reads the Excel file at `/data/data/agent_test_codebase/GitTaskBench/queries/Eparse_03/input/Eparse_03_input.xlsx` and converts it to a flat JSON array where each element represents a cell in the Excel file. The output is saved to `output.json`.

### Structured JSON Conversion

```bash
python excel_to_structured_json.py
```

This script reads the same Excel file but converts it to a structured JSON object that groups data by sheets and tables. The output is saved to `output_structured.json`.

## JSON Structure

### Flat JSON

The flat JSON output is an array of objects, where each object represents a cell in the Excel file with the following properties:

- `row`: The row index (0-based)
- `column`: The column index (0-based)
- `value`: The cell value
- `type`: The data type of the cell value
- `c_header`: The column header
- `r_header`: The row header
- `excel_RC`: The Excel cell reference (e.g., A1)
- `name`: The table name
- `sheet`: The sheet name
- `f_name`: The file name

### Structured JSON

The structured JSON output is an object with the following structure:

```json
{
  "file_name": "Eparse_03_input.xlsx",
  "sheets": {
    "SheetName1": [
      {
        "name": "Table_0",
        "rows": 13,
        "columns": 3,
        "data": [
          {
            "row": 0,
            "column": 0,
            "value": "1",
            "type": "<class 'numpy.int64'>",
            "c_header": "1",
            "r_header": "1",
            "excel_RC": "A1",
            "name": "Table_0",
            "sheet": "SheetName1",
            "f_name": "Eparse_03_input.xlsx"
          },
          // More cells...
        ]
      },
      // More tables...
    ],
    // More sheets...
  }
}
```

## Customization

You can modify the scripts to customize the JSON output format or to process different Excel files. Just update the file paths and the serialization logic as needed.