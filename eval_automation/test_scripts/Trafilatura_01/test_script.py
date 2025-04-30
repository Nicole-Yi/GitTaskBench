import argparse
import json
from trafilatura import fetch_url, extract
from sklearn.metrics import precision_score, recall_score
import re
import numpy as np

# 计算 precision 和 recall 的函数
def compute_precision_recall(extracted_content, ground_truth):
    # 通过简单的字符级别对比，转为字符的集合
    extracted_chars = set(extracted_content.lower())
    ground_truth_chars = set(ground_truth.lower())

    # 计算交集和并集
    intersection = extracted_chars.intersection(ground_truth_chars)
    precision = len(intersection) / len(extracted_chars) if len(extracted_chars) > 0 else 0
    recall = len(intersection) / len(ground_truth_chars) if len(ground_truth_chars) > 0 else 0

    return precision, recall

# 提取内容并生成摘要的函数
def extract_content_and_summary(url, output_path):
    # 获取网页内容
    downloaded = fetch_url(url)
    
    # 提取网页正文
    extracted_content = extract(downloaded)
    
    # 打开已有的JSON文件，获取人工标注的正文
    with open(output_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    ground_truth = data.get("ground_truth", "")
    
    # 计算 precision 和 recall
    precision, recall = compute_precision_recall(extracted_content, ground_truth)
    
    # 判断是否通过精确度标准
    is_passed = precision >= 0.92
    match_result = ":white_check_mark:" if is_passed else ":x:"
    
    if not is_passed:
        print(":x: 不通过：精确度低于 92%")
    
    # 输出提取内容和评估结果
    output_data = {
        "url": url,
        "extracted_content": extracted_content,
        "ground_truth": ground_truth,
        "precision": precision,
        "recall": recall,
        "match": match_result,
        "precision_threshold": 0.92,
        "passed": is_passed
    }

    # 将结果写入指定路径
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(f":white_check_mark: 完成提取与评估，结果已保存到 {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="提取新闻网页正文并与人工标注内容对比")
    parser.add_argument("--url", required=True, help="新闻网页的 URL")
    parser.add_argument("--output", required=True, help="保存提取结果的 JSON 文件路径")
    
    args = parser.parse_args()
    extract_content_and_summary(args.url, args.output) 