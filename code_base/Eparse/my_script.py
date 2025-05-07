
import pandas as pd
from eparse.core import get_df_from_file

input_file = '/data/data/agent_test_codebase/GitTaskBench/queries/Eparse_02/input/Eparse_02_input.xlsx'
sheet = 'Sheet1'

output_dir = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Eparse_02/output.txt'

# Extract parsed tables
tables = list(get_df_from_file(input_file, sheet=[sheet]))

# Print tables to output file
with open(output_dir, 'w') as file:
    for table, _, table_name, _ in tables:
        file.write(f'Table {table_name}:\n{table.to_string()}\n\n')

print('Script executed successfully!')