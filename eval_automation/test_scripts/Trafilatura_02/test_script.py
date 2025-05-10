import os
import argparse
import numpy as np
import json
import datetime

# 引入Levenshtein距离的计算函数
from Levenshtein import distance as levenshtein_distance

def evaluate_extraction(pred_path, gt_path):
    # 固定阈值
    threshold = 0.5  # 编辑距离低于这个阈值即认为预测成功

    # 检查文件是否存在
    def check_file_exists(file_path):
        if not os.path.isfile(file_path):
            print(f"❌ 错误: 文件不存在: {file_path}")
            exit(1)
        if os.path.getsize(file_path) == 0:
            print(f"❌ 错误: 文件为空: {file_path}")
            exit(1)

    # 检查文件
    check_file_exists(pred_path)
    check_file_exists(gt_path)

    # 读取预测结果
    with open(pred_path, 'r', encoding='utf-8') as f:
        pred_text = f.read()
    
    # 读取ground truth
    with open(gt_path, 'r', encoding='utf-8') as f:
        gt_text = f.read()
    
    # 计算编辑距离
    edit_distance = levenshtein_distance(pred_text, gt_text)
    max_len = max(len(pred_text), len(gt_text))
    
    # 计算编辑距离比率
    edit_distance_ratio = edit_distance / max_len if max_len > 0 else 0

    # 输出编辑距离比率
    print(f"编辑距离比率（Edit Distance Ratio）: {edit_distance_ratio:.4f}")

    # 判断是否达到阈值
    if edit_distance_ratio <= threshold:
        print("✅ 正确完成")
    else:
        print("❌ 提取有误")

    return edit_distance_ratio

def main():
    parser = argparse.ArgumentParser(description="Evaluate the edit distance between extracted and ground truth markdown content.")
    parser.add_argument('--pred_path', type=str, required=True, help='Path to the extracted prediction markdown file')
    parser.add_argument('--gt_path', type=str, required=True, help='Path to the ground truth markdown file')
    parser.add_argument('--result', type=str, required=True, help='Path to save the result in jsonl format')

    args = parser.parse_args()

    # 计算提取准确度（编辑距离比率）
    edit_distance_ratio = evaluate_extraction(pred_path=args.pred_path, gt_path=args.gt_path)

    # 保存结果
    result = {
        "Process": True,
        "Result": edit_distance_ratio <= 0.5,  # 判断编辑距离比率是否低于阈值
        "TimePoint": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "comments": f"编辑距离比率: {edit_distance_ratio:.4f} {'满足' if edit_distance_ratio <= 0.5 else '不满足'} 50% 精度要求"
    }

    # 如果文件存在，追加写入，否则创建新文件
    if os.path.exists(args.result):
        with open(args.result, 'a', encoding='utf-8') as f:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')
    else:
        with open(args.result, 'w', encoding='utf-8') as f:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')

    print(f"结果已保存到: {args.result}")

if __name__ == "__main__":
    main()
