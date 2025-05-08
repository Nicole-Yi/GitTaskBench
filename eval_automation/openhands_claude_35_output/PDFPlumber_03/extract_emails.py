import pdfplumber
import re
import os

def extract_emails_from_pdf(pdf_path, output_path):
    # 编译邮箱地址的正则表达式
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    # 打开PDF文件
    with pdfplumber.open(pdf_path) as pdf:
        # 存储找到的所有邮箱地址
        emails = set()
        
        # 遍历每一页
        for page in pdf.pages:
            # 提取文本
            text = page.extract_text()
            if text:
                # 查找所有邮箱地址
                found_emails = re.findall(email_pattern, text)
                emails.update(found_emails)
    
    # 将邮箱地址写入输出文件
    with open(output_path, 'w') as f:
        for email in sorted(emails):
            f.write(email + '\n')

if __name__ == '__main__':
    # 输入PDF文件路径
    pdf_path = '/data/data/agent_test_codebase/GitTaskBench/queries/PDFPlumber_03/input/PDFPlumber_03_input.pdf'
    # 输出文件路径
    output_path = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/PDFPlumber_03/output.txt'
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 提取邮箱地址
    extract_emails_from_pdf(pdf_path, output_path)