import argparse
import os
import xml.etree.ElementTree as ET
import csv
import json
from datetime import datetime

def check_file_valid(file_path: str) -> bool:
    """检查文件是否存在且非空"""
    if not os.path.isfile(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return False
    if os.path.getsize(file_path) == 0:
        print(f"❌ 文件为空: {file_path}")
        return False
    return True

def parse_xml(file_path):
    """解析 Scrapy 输出的 XML 文件"""
    tree = ET.parse(file_path)
    root = tree.getroot()
    records = []
    for item in root.findall("item"):
        record = {}
        for field in item:
            record[field.tag] = field.text or ""
        records.append(record)
    return records

def parse_csv(file_path):
    """读取 Ground Truth 的 CSV 文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def evaluate_scraping_xml(pred_file, gt_file, threshold=0.95, result_file=None):
    """评估 Scrapy XML 输出与 Ground Truth CSV 之间的字段级准确率"""
    if not check_file_valid(pred_file) or not check_file_valid(gt_file):
        return {}, False

    preds = parse_xml(pred_file)
    gts = parse_csv(gt_file)

    if len(preds) != len(gts):
        print(f"⚠️ 预测结果与标注数据长度不一致（预测 {len(preds)} 条，真实 {len(gts)} 条），按最小数量进行比较。")

    num_samples = min(len(preds), len(gts))

    if not preds or not gts:
        print("❌ 错误：预测或标准数据为空。")
        return {}, False

    fields = preds[0].keys()
    correct_counts = {field: 0 for field in fields}

    for i in range(num_samples):
        for field in fields:
            if field in gts[i] and preds[i].get(field, "").strip() == gts[i][field].strip():
                correct_counts[field] += 1

    accuracies = {field: correct_counts[field] / num_samples for field in fields}

    # 输出结果
    for field, acc in accuracies.items():
        print(f"字段 '{field}' 的准确率: {acc:.4f}")

    success = all(acc >= threshold for acc in accuracies.values())

    if success:
        print("✅ 验证通过: 所有字段准确度大于95%")
    else:
        print("❌ 验证不通过: 存在字段准确度小于95%")

    # 保存结果
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
    parser = argparse.ArgumentParser(description="Evaluate Scrapy XML output against ground truth CSV.")
    parser.add_argument('--pred_file', type=str, required=True, help="Path to the predicted XML file")
    parser.add_argument('--gt_file', type=str, required=True, help="Path to the ground truth CSV file")
    parser.add_argument('--threshold', type=float, default=0.95, help="Accuracy threshold per field")
    parser.add_argument('--result', type=str, required=False, help="Save results to a JSONL file")

    args = parser.parse_args()

    evaluate_scraping_xml(args.pred_file, args.gt_file, args.threshold, args.result)

if __name__ == "__main__":
    main()
