import argparse
import json
import os
from datetime import datetime


def check_file_valid(file_path: str) -> bool:
    if not os.path.isfile(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return False
    if os.path.getsize(file_path) == 0:
        print(f"❌ 文件为空: {file_path}")
        return False
    return True


def evaluate_scrapy_output(pred_path: str, truth_path: str, result_path: str = None) -> bool:
    threshold = 0.95
    process_success = check_file_valid(pred_path) and check_file_valid(truth_path)

    if not process_success:
        result = {
            "Process": False,
            "Result": False,
            "TimePoint": datetime.now().isoformat(),
            "comments": f"❌ 文件不存在或为空: pred={pred_path}, truth={truth_path}"
        }
        if result_path:
            with open(result_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(result, ensure_ascii=False, default=str) + "\n")
        return False

    try:
        with open(pred_path, "r", encoding="utf-8") as f_pred, \
             open(truth_path, "r", encoding="utf-8") as f_true:
            pred_lines = [json.loads(line.strip()) for line in f_pred if line.strip()]
            true_lines = [json.loads(line.strip()) for line in f_true if line.strip()]

        if len(pred_lines) != len(true_lines):
            print(f"⚠️ 抓取结果与标注数量不一致（预测 {len(pred_lines)} 条，真实 {len(true_lines)} 条）")

        total_fields = 0
        correct_fields = 0

        for pred, true in zip(pred_lines, true_lines):
            for field in ["author", "text"]:
                total_fields += 1
                if pred.get(field, "").strip() == true.get(field, "").strip():
                    correct_fields += 1

        accuracy = correct_fields / total_fields if total_fields else 0
        print(f"📊 字段级准确率 (Field Accuracy): {accuracy:.2%}")
        result_passed = accuracy >= threshold
        print("✅ 提取有效，字段级准确率>=95%" if result_passed else "❌ 提取无效")

        # 保存结果
        if result_path:
            result = {
                "Process": True,
                "Result": result_passed,
                "TimePoint": datetime.now().isoformat(),
                "comments": f"字段级准确率: {accuracy:.4f}，{'满足' if result_passed else '不满足'} 95% 阈值"
            }
            with open(result_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(result, ensure_ascii=False, default=str) + "\n")

        return result_passed

    except Exception as e:
        print(f"❌ 运行异常: {e}")
        if result_path:
            result = {
                "Process": True,
                "Result": False,
                "TimePoint": datetime.now().isoformat(),
                "comments": f"运行异常: {str(e)}"
            }
            with open(result_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(result, ensure_ascii=False, default=str) + "\n")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="评估 Scrapy 抓取结果的字段级准确率")
    parser.add_argument("--pred_file", type=str, required=True, help="预测结果（JSONL）路径")
    parser.add_argument("--truth_file", type=str, required=True, help="标注数据（JSONL）路径")
    parser.add_argument("--result", type=str, required=False, help="保存结果的JSONL文件路径")

    args = parser.parse_args()
    success = evaluate_scrapy_output(args.pred_file, args.truth_file, args.result)
    if not success:
        exit(1)
