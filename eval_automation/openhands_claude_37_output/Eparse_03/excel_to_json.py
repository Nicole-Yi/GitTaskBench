#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to convert Excel file to JSON format using Eparse
"""

import json
import os
from pathlib import Path

from eparse.core import get_df_from_file, df_serialize_table

def excel_to_json(excel_file_path, output_file_path):
    """
    Convert Excel file to JSON format using Eparse
    
    Args:
        excel_file_path (str): Path to the Excel file
        output_file_path (str): Path to save the JSON output
    """
    # Get all tables from the Excel file
    all_data = []
    
    # Process each table found in the Excel file
    for table in get_df_from_file(excel_file_path):
        # Serialize the table data
        serialized_data = df_serialize_table(
            table[0],  # The DataFrame
            name=f"Table_{len(all_data)}",  # Give a name to the table
            sheet=table[1],  # Sheet name
            f_name=os.path.basename(excel_file_path)  # File name
        )
        
        # Convert to list if it's not already
        if not isinstance(serialized_data, list):
            serialized_data = [serialized_data]
            
        # Add to our collection
        all_data.extend(serialized_data)
    
    # Write the data to a JSON file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    
    print(f"Converted {excel_file_path} to JSON format at {output_file_path}")
    return all_data

if __name__ == "__main__":
    # Input and output file paths
    excel_file = "/data/data/agent_test_codebase/GitTaskBench/queries/Eparse_03/input/Eparse_03_input.xlsx"
    output_file = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Eparse_03/output.json"
    
    # Convert Excel to JSON
    excel_to_json(excel_file, output_file)