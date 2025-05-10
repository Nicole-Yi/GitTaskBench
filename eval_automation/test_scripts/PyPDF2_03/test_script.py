import argparse
import json
from datetime import datetime

TARGET_FIELDS = {"Author", "Title", "CreationDate"}

def load_truth_metadata(file_path):
    metadata = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if ": " in line:
                key, value = line.strip().split(": ", 1)
                key = key.strip().lstrip("/")
                metadata[key] = value.strip()
    return metadata

def load_pred_metadata(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            return {}

def compute_recall(pred_value, truth_value):
    pred_chars = set(pred_value.lower())
    truth_chars = set(truth_value.lower())
    if not truth_chars:
        return 1.0
    return len(pred_chars & truth_chars) / len(truth_chars)

def evaluate(pred_file, truth_file, result_file):
    pred_metadata = load_pred_metadata(pred_file)
    truth_metadata = load_truth_metadata(truth_file)

    total_fields = len(TARGET_FIELDS)
    passed_fields = 0
    comments = []

    for key in TARGET_FIELDS:
        truth_value = truth_metadata.get(key, "")
        pred_value = str(pred_metadata.get(key, ""))
        recall = compute_recall(pred_value, truth_value)

        if recall >= 0.5:
            passed_fields += 1
            comments.append(f"✅ 字段 {key} 召回率: {recall:.2f} >= 0.5")
        else:
            comments.append(f"❌ 字段 {key} 召回率: {recall:.2f} < 0.5，预测: {pred_value}，应为: {truth_value}")

    pass_ratio = passed_fields / total_fields if total_fields else 0
    overall_pass = pass_ratio >= 0.5
    comments.append(f"📊 字段通过率: {pass_ratio:.2f} ({passed_fields}/{total_fields})")
    comments.append("✅ 测试通过！" if overall_pass else "❌ 测试未通过")

    for c in comments:
        print(c)

    result_data = {
        "Process": True,
        "Result": overall_pass,
        "TimePoint": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "comments": " ".join(comments)
    }

    with open(result_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(result_data, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pred_file", type=str, required=True, help="预测结果 JSON 文件路径")
    parser.add_argument("--truth_file", type=str, required=True, help="标准答案 TXT 文件路径")
    parser.add_argument("--result", type=str, required=True, help="评测结果输出 JSONL 文件")
    args = parser.parse_args()

    evaluate(args.pred_file, args.truth_file, args.result)
