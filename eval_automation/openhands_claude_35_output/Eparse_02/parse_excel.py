from pathlib import Path
from eparse.core import get_df_from_file, df_serialize_table

def parse_excel_to_txt(excel_path, output_path):
    """Parse Excel file and save serialized data to txt file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        for table in get_df_from_file(excel_path):
            for row in df_serialize_table(table[0]):
                f.write(str(row) + '\n')

if __name__ == '__main__':
    excel_path = '/data/data/agent_test_codebase/GitTaskBench/queries/Eparse_02/input/Eparse_02_input.xlsx'
    output_path = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Eparse_02/output.txt'
    
    # 确保输出目录存在
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # 解析Excel并保存到txt文件
    parse_excel_to_txt(excel_path, output_path)
    print(f'Excel file has been parsed and saved to {output_path}')