import argparse
import csv
import json
import os
from datetime import datetime

def load_csv(file_path):
    try:
        rows = []
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(row)
        return rows, None
    except Exception as e:
        return [], str(e)

def evaluate(pred_file, truth_file):
    pred_rows, pred_err = load_csv(pred_file)
    truth_rows, truth_err = load_csv(truth_file)

    process_ok = True
    comments = ""

    if pred_err:
        comments += f"[预测文件读取失败] {pred_err}\n"
        process_ok = False
    if truth_err:
        comments += f"[GT文件读取失败] {truth_err}\n"
        process_ok = False

    if not process_ok:
        return {
            "Process": False,
            "Result": False,
            "TimePoint": datetime.now().isoformat(),
            "comments": comments.strip()
        }

    total = min(len(pred_rows), len(truth_rows))
    if total == 0:
        return {
            "Process": True,
            "Result": False,
            "TimePoint": datetime.now().isoformat(),
            "comments": "⚠️ 没有找到任何数据行！"
        }

    correct = 0
    for pred_row, truth_row in zip(pred_rows, truth_rows):
        if pred_row == truth_row:
            correct += 1

    match_rate = (correct / total) * 100
    passed = match_rate >= 98
    result_msg = (
        f"整体表格行列内容匹配率：{match_rate:.2f}%\n"
        + ("✅ 测试通过！" if passed else "❌ 测试未通过！")
    )

    return {
        "Process": True,
        "Result": passed,
        "TimePoint": datetime.now().isoformat(),
        "comments": result_msg
    }

def append_result_to_jsonl(result_path, result_dict):
    os.makedirs(os.path.dirname(result_path), exist_ok=True)
    with open(result_path, "a", encoding="utf-8") as f:
        json.dump(result_dict, f, ensure_ascii=False, default=str)
        f.write("\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pred_file", type=str, required=True, help="提取出的整体表格路径")
    parser.add_argument("--truth_file", type=str, required=True, help="标准整体表格路径")
    parser.add_argument("--result", type=str, required=True, help="结果输出 JSONL 文件路径")
    args = parser.parse_args()

    result_dict = evaluate(args.pred_file, args.truth_file)
    append_result_to_jsonl(args.result, result_dict)

    print("[评估完成] 结果摘要：")
    print(json.dumps(result_dict, ensure_ascii=False, indent=2, default=str))
