import pdfplumber

# 打开PDF文件
pdf_path = "/data/data/agent_test_codebase/GitTaskBench/queries/PDFPlumber_01/input/PDFPlumber_01_input.pdf"
output_path = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/PDFPlumber_01/output.txt"

with pdfplumber.open(pdf_path) as pdf:
    # 获取第一页
    first_page = pdf.pages[0]
    
    # 提取文本内容
    text = first_page.extract_text()
    
    # 将文本写入输出文件
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)