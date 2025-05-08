#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to convert Excel file to structured JSON format using Eparse
"""

import json
import os
from collections import defaultdict
from pathlib import Path

from eparse.core import get_df_from_file, df_serialize_table

def excel_to_structured_json(excel_file_path, output_file_path):
    """
    Convert Excel file to structured JSON format using Eparse
    
    Args:
        excel_file_path (str): Path to the Excel file
        output_file_path (str): Path to save the JSON output
    """
    # Get all tables from the Excel file
    structured_data = {
        "file_name": os.path.basename(excel_file_path),
        "sheets": defaultdict(list)
    }
    
    table_count = 0
    
    # Process each table found in the Excel file
    for table in get_df_from_file(excel_file_path):
        df = table[0]  # The DataFrame
        sheet_name = table[1]  # Sheet name
        
        # Create a table name
        table_name = f"Table_{table_count}"
        table_count += 1
        
        # Serialize the table data
        serialized_data = df_serialize_table(
            df,
            name=table_name,
            sheet=sheet_name,
            f_name=os.path.basename(excel_file_path)
        )
        
        # Convert to list if it's not already
        if not isinstance(serialized_data, list):
            serialized_data = [serialized_data]
        
        # Group data by table
        table_data = {
            "name": table_name,
            "rows": len(df),
            "columns": len(df.columns),
            "data": serialized_data
        }
        
        # Add to our collection
        structured_data["sheets"][sheet_name].append(table_data)
    
    # Write the data to a JSON file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(structured_data, f, indent=2, ensure_ascii=False)
    
    print(f"Converted {excel_file_path} to structured JSON format at {output_file_path}")
    return structured_data

if __name__ == "__main__":
    # Input and output file paths
    excel_file = "/data/data/agent_test_codebase/GitTaskBench/queries/Eparse_03/input/Eparse_03_input.xlsx"
    output_file = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Eparse_03/output_structured.json"
    
    # Convert Excel to structured JSON
    excel_to_structured_json(excel_file, output_file)