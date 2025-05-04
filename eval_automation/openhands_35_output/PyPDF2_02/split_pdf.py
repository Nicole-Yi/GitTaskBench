from PyPDF2 import PdfReader, PdfWriter
import os

def split_pdf(input_path, output_dir):
    # 创建输出目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)
    
    # 读取PDF文件
    reader = PdfReader(input_path)
    total_pages = len(reader.pages)
    
    # 遍历每一页并创建新的PDF文件
    for page_num in range(total_pages):
        writer = PdfWriter()
        writer.add_page(reader.pages[page_num])
        
        # 生成输出文件名
        output_filename = os.path.join(output_dir, f'output_{page_num + 1:02d}.pdf')
        
        # 保存单页PDF
        with open(output_filename, 'wb') as output_file:
            writer.write(output_file)
        
        print(f'Created: {output_filename}')

if __name__ == '__main__':
    input_path = '/data/data/agent_test_codebase/GitTaskBench/queries/PyPDF2_02/input/PyPDF2_02_input.pdf'
    output_dir = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/PyPDF2_02'
    
    split_pdf(input_path, output_dir)
    print('PDF splitting completed!')