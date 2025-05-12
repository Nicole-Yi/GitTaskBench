import sys
sys.path.append("/data/data/agent_test_codebase/GitTaskBench/code_base/Trafilatura")
from trafilatura.core import extract
from trafilatura.downloads import fetch_url
import os

url = "https://finance.sina.com.cn/zt_d/subject-1745887515/"
output_dir = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Trafilatura_02"
os.makedirs(output_dir, exist_ok=True)

html = fetch_url(url)
result = extract(html, output_format="markdown")
with open(f"{output_dir}/output.md", "w", encoding="utf-8") as f:
    f.write(result or "No content extracted")
print("Extraction completed")