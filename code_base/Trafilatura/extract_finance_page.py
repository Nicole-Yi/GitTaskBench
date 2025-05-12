import sys
sys.path.append("/data/data/agent_test_codebase/GitTaskBench/code_base/Trafilatura")
from trafilatura import fetch_url, extract
import os

# URL to extract
url = "https://finance.sina.com.cn/zt_d/subject-1745887515/"

# Output directory and filename
output_dir = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Trafilatura_02"
output_file = os.path.join(output_dir, "output.md")

# Fetch and extract content
downloaded = fetch_url(url)
result = extract(downloaded, output_format="markdown", with_metadata=True)

# Save to file
with open(output_file, "w", encoding="utf-8") as f:
    f.write(result)

print(f"Content extracted and saved to {output_file}")