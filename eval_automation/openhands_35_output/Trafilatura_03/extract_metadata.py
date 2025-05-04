from trafilatura import extract_metadata
import json
import requests

# 目标URL
url = 'https://www.cnprose.com/article-detail/WJaljpMN'

# 下载网页内容
try:
    response = requests.get(url, timeout=10)
    downloaded = response.text
except requests.exceptions.RequestException as e:
    print(f"下载网页时出错: {e}")
    downloaded = None

if downloaded:
    # 提取元数据
    metadata = extract_metadata(downloaded)
    
    # 将元数据转换为字典
    metadata_dict = {}
    if metadata:
        # 获取所有可能的属性
        attrs = ['title', 'author', 'date', 'description', 'categories', 'tags', 'sitename', 'url']
        for attr in attrs:
            value = getattr(metadata, attr, None)
            if value:  # 只保存非空值
                metadata_dict[attr] = value

    # 将结果保存为txt文件
    output_path = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Trafilatura_03/output.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(metadata_dict, f, ensure_ascii=False, indent=2)
    print(f"元数据已保存到: {output_path}")
else:
    print("无法下载网页内容")