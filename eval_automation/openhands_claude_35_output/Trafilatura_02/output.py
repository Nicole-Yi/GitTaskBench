import os
import time
from trafilatura import fetch_url, extract
from urllib3.util.timeout import Timeout

# 设置要抓取的URL
url = 'https://finance.sina.com.cn/zt_d/subject-1745887515/'

# 设置代理
os.environ['http_proxy'] = 'http://127.0.0.1:51589'
os.environ['https_proxy'] = 'http://127.0.0.1:51589'

# 设置超时时间
timeout = Timeout(connect=10.0, read=30.0)

# 下载网页内容，最多重试3次
max_retries = 3
downloaded = None

for attempt in range(max_retries):
    try:
        downloaded = fetch_url(url, timeout=timeout)
        if downloaded:
            break
    except Exception as e:
        print(f"Attempt {attempt + 1} failed: {str(e)}")
        if attempt < max_retries - 1:
            time.sleep(2)  # 等待2秒后重试
        continue

if not downloaded:
    print("Failed to download the webpage after all attempts")

# 提取内容并转换为markdown格式
result = extract(downloaded, output_format='markdown', include_comments=False)

# 将结果保存到文件
output_file = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Trafilatura_02/output.md'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(result if result else "Failed to extract content")