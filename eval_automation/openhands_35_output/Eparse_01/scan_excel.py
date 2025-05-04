import os
from pathlib import Path
import pandas as pd
import openpyxl

def scan_excel_files(input_dir, output_file):
    # 创建输出目录（如果不存在）
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # 存储结果的列表
    results = []
    
    # 遍历目录下的所有文件
    for file_path in Path(input_dir).rglob("*.xls*"):  # 匹配.xls和.xlsx文件
        try:
            # 打开Excel文件
            wb = openpyxl.load_workbook(file_path, read_only=True)
            
            # 获取所有sheet名称
            sheet_names = wb.sheetnames
            
            # 记录文件信息
            file_info = {
                "file_name": file_path.name,
                "file_path": str(file_path),
                "sheets": sheet_names
            }
            
            results.append(file_info)
            
            # 关闭工作簿
            wb.close()
            
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
    
    # 将结果写入文本文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Excel Files and Sheets Information:\n")
        f.write("=" * 50 + "\n\n")
        
        for result in results:
            f.write(f"File: {result['file_name']}\n")
            f.write(f"Path: {result['file_path']}\n")
            f.write("Sheets:\n")
            for sheet in result['sheets']:
                f.write(f"  - {sheet}\n")
            f.write("\n")

if __name__ == "__main__":
    input_dir = "/data/data/agent_test_codebase/GitTaskBench/queries/Eparse_01/input/Eparse_01_input"
    output_file = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Eparse_01/output.txt"
    
    scan_excel_files(input_dir, output_file)
    print(f"Scan completed. Results saved to {output_file}")