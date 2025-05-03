import pdfplumber
import csv
import os

def extract_tables_from_pdf(pdf_path, output_path):
    all_tables = []
    
    with pdfplumber.open(pdf_path) as pdf:
        # 只处理前两页
        for page_num in range(min(2, len(pdf.pages))):
            page = pdf.pages[page_num]
            tables = page.extract_tables()
            
            for table in tables:
                # 过滤掉空行和全None的行
                filtered_table = [
                    [str(cell).strip() if cell is not None else "" for cell in row]
                    for row in table
                    if any(cell is not None and str(cell).strip() for cell in row)
                ]
                if filtered_table:
                    all_tables.extend(filtered_table)
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 将所有表格写入CSV文件
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(all_tables)

if __name__ == "__main__":
    input_pdf = "/data/data/agent_test_codebase/GitTaskBench/queries/PDFPlumber_02/input/PDFPlumber_02_input.pdf"
    output_csv = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/PDFPlumber_02/output.csv"
    
    extract_tables_from_pdf(input_pdf, output_csv)
    print(f"Tables have been extracted and saved to {output_csv}")