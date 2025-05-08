import json
from eparse.core import get_df_from_file, df_serialize_table
from pathlib import Path

input_file = '/data/data/agent_test_codebase/GitTaskBench/queries/Eparse_03/input/Eparse_03_input.xlsx'
output_dir = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Eparse_03/'

# Load excel file
excel_tables = get_df_from_file(input_file)

# Convert each table to JSON
output_data = []
for table in excel_tables:
    serialized_table = [row for row in df_serialize_table(table[0])]
    output_data.append(serialized_table)

# Save JSON to output directory
output_path = Path(output_dir) / 'output.json'
with output_path.open('w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=4)

print(f'JSON output saved to {output_path}')
