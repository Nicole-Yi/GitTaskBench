import argparse
import os
import xml.etree.ElementTree as ET
import csv
import json
from datetime import datetime

def check_file_valid(file_path: str) -> bool:
    if not os.path.isfile(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return False
    if os.path.getsize(file_path) == 0:
        print(f"❌ 文件为空: {file_path}")
        return False
    return True

def parse_xml(file_path):
    """解析 quotes XML 文件，结构为 <quotes><quote><text>...</text><author>...</author></quote>...</quotes>"""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"❌ XML 解析错误: {e}")
        return []

    records = []
    for quote_elem in root.findall("quote"):
        text_elem = quote_elem.find("text")
        author_elem = quote_elem.find("author")
        if text_elem is None or author_elem is None:
            continue  # 跳过不完整的 quote

        record = {
            "text": (text_elem.text or "").strip(),
            "author": (author_elem.text or "").strip()
        }

        # 只收录有内容的记录
        if record["text"] and record["author"]:
            records.append(record)
    return records

def parse_csv(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            records = []
            for row in reader:
                if "text" in row and "author" in row:
                    records.append({
                        "text": row["text"].strip(),
                        "author": row["author"].strip()
                    })
            return records
    except Exception as e:
        print(f"❌ CSV 读取失败: {e}")
        return []

def evaluate_scraping_xml(pred_file, gt_file, threshold=0.95, result_file=None):
    if not check_file_valid(pred_file) or not check_file_valid(gt_file):
        return {}, False

    preds = parse_xml(pred_file)
    gts = parse_csv(gt_file)

    if len(preds) != len(gts):
        print(f"⚠️ 预测结果与标注数据长度不一致（预测 {len(preds)} 条，真实 {len(gts)} 条），按最小数量进行比较。")

    num_samples = min(len(preds), len(gts))
    if num_samples == 0:
        print("❌ 错误：无可比对的数据。")
        return {}, False

    fields = ["author", "text"]
    correct_counts = {field: 0 for field in fields}

    for i in range(num_samples):
        for field in fields:
            pred_val = preds[i].get(field, "").strip()
            gt_val = gts[i].get(field, "").strip()
            if pred_val == gt_val:
                correct_counts[field] += 1

    accuracies = {field: correct_counts[field] / num_samples for field in fields}

    for field, acc in accuracies.items():
        print(f"字段 '{field}' 的准确率: {acc:.4f}")

    success = all(acc >= threshold for acc in accuracies.values())
    print("✅ 验证通过: 所有字段准确度大于等于 95%" if success else "❌ 验证不通过: 存在字段准确度小于 95%")

    if result_file:
        result = {
            "Process": True,
            "Results": success,
            "TimePoint": datetime.now().isoformat(),
            "comments": f"字段级准确率: {accuracies}, {'满足' if success else '不满足'} 95% 阈值"
        }
        with open(result_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(result, ensure_ascii=False, default=str) + "\n")

    return accuracies, success

def main():
    parser = argparse.ArgumentParser(description="评估 XML 提取结果与 Ground Truth CSV 的准确率。")
    parser.add_argument('--pred_file', type=str, required=True, help="预测 XML 文件路径")
    parser.add_argument('--gt_file', type=str, required=True, help="Ground truth CSV 文件路径")
    parser.add_argument('--threshold', type=float, default=0.95, help="字段准确率阈值")
    parser.add_argument('--result', type=str, required=False, help="结果保存的 JSONL 文件路径")
    args = parser.parse_args()

    evaluate_scraping_xml(args.pred_file, args.gt_file, args.threshold, args.result)

if __name__ == "__main__":
    main()
