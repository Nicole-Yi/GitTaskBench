import argparse
import sys
import os
import json
from datetime import datetime

def compute_precision_recall(extracted_content, ground_truth):
    """计算precision和recall的函数"""
    extracted_chars = set(extracted_content.lower())
    ground_truth_chars = set(ground_truth.lower())

    intersection = extracted_chars & ground_truth_chars
    precision = len(intersection) / len(extracted_chars) if extracted_chars else 0
    recall = len(intersection) / len(ground_truth_chars) if ground_truth_chars else 0

    return precision, recall

def check_file_exists(file_path):
    """检查文件是否存在，并且不为空"""
    if not os.path.isfile(file_path):
        print(f"❌ 错误: 文件不存在: {file_path}")
        return False
    if os.path.getsize(file_path) == 0:
        print(f"❌ 错误: 文件为空: {file_path}")
        return False
    return True

def compare_txt_files(extracted_txt_path, ground_truth_txt_path, result_file):
    try:
        # 检查文件是否存在且不为空
        process_status = check_file_exists(extracted_txt_path) and check_file_exists(ground_truth_txt_path)

        # 记录当前时间
        time_point = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        # 读取提取的文本文件和ground truth文本文件
        with open(extracted_txt_path, "r", encoding="utf-8") as f:
            extracted_message = f.read().strip()

        with open(ground_truth_txt_path, "r", encoding="utf-8") as f:
            ground_truth_message = f.read().strip()

        # 计算precision和recall
        precision, recall = compute_precision_recall(extracted_message, ground_truth_message)
        passed = precision >= 0.92
        match_result = ":white_check_mark:" if passed else ":x:"

        # 输出结果
        print(f"🔍 精度: {precision:.4f} | 召回率: {recall:.4f}")
        print(f"结果: {match_result} 精确度 {precision:.4f} {'满足' if passed else '不满足'} 92%")

        results_status = passed
        comments = f"精确度 {precision:.4f} {'满足' if passed else '不满足'} 92%"

        # 写入jsonl结果
        result_data = {
            "Process": process_status,
            "Result": results_status,
            "TimePoint": time_point,
            "comments": comments
        }

        # 如果文件已存在，进行追加；如果不存在，新建
        with open(result_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(result_data, ensure_ascii=False, default=str) + "\n")

        if not passed:
            sys.exit(1)

    except Exception as e:
        print(f"❌ 测试异常: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="比较提取文本与ground truth文件内容")
    parser.add_argument("--extracted_txt", required=True, help="提取的txt文件路径")
    parser.add_argument("--ground_truth_txt", required=True, help="ground truth txt文件路径")
    parser.add_argument("--result", required=True, help="存储测试结果的jsonl文件路径")
    
    args = parser.parse_args()

    compare_txt_files(args.extracted_txt, args.ground_truth_txt, args.result)

if __name__ == "__main__":
    main()
