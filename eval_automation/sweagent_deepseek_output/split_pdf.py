from pypdf import PdfReader, PdfWriter
import os

input_path = "/data/data/agent_test_codebase/GitTaskBench/queries/PyPDF2_02/input/PyPDF2_02_input.pdf"
output_dir = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/PyPDF2_02"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

reader = PdfReader(input_path)

for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    
    output_path = os.path.join(output_dir, f"output_{i+1:02d}.pdf")
    with open(output_path, "wb") as output_pdf:
        writer.write(output_pdf)

print(f"Split {len(reader.pages)} pages into separate PDF files in {output_dir}")