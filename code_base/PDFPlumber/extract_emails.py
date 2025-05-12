
import re
import sys
from PyPDF2 import PdfReader

def extract_emails_from_pdf(pdf_path, output_path):
    emails = set()
    reader = PdfReader(pdf_path)
    
    for page in reader.pages:
        text = page.extract_text()
        if text:
            found_emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
            emails.update(found_emails)
    
    with open(output_path, 'w') as f:
        for email in sorted(emails):
            f.write(email + '\n')
    return len(emails)

if __name__ == "__main__":
    input_pdf = '/data/data/agent_test_codebase/GitTaskBench/queries/PDFPlumber_03/input/PDFPlumber_03_input.pdf'
    output_txt = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/PDFPlumber_03/output.txt'
    
    count = extract_emails_from_pdf(input_pdf, output_txt)
    print(f"Extracted {count} email addresses to {output_txt}")