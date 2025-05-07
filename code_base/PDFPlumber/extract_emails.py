
import pdfplumber
import re

# Define file paths
input_pdf = '/data/data/agent_test_codebase/GitTaskBench/queries/PDFPlumber_03/input/PDFPlumber_03_input.pdf'
output_txt = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/PDFPlumber_03/output.txt'

# Regular expression pattern for matching email addresses
email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')

# Open the PDF file
def extract_emails_from_pdf():
    emails = set()
    with pdfplumber.open(input_pdf) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                emails.update(email_pattern.findall(text))

    # Save the emails to a text file
    with open(output_txt, 'w') as f:
        for email in emails:
            f.write(email + '\n')

if __name__ == "__main__":
    extract_emails_from_pdf()
    print("Email extraction completed.")