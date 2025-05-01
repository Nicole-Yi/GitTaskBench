import os
import argparse

def evaluate_extraction(pred_path, gt_path):
    # 固定阈值
    threshold = 0.95

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
    
    # 计算字符级准确率
    match_count = sum(1 for p, g in zip(pred_text, gt_text) if p == g)
    total_count = len(gt_text)
    char_accuracy = match_count / total_count if total_count > 0 else 0

    # 输出准确率
    print(f"字符级准确率（Char Accuracy）: {char_accuracy:.4f}")

    # 判断是否达到阈值
    if char_accuracy >= threshold:
        print("✅ 正确完成")
    else:
        print("❌ 提取有误")

    return char_accuracy

def main():
    parser = argparse.ArgumentParser(description="Evaluate the character-level accuracy of markdown content extraction.")
    parser.add_argument('--pred_path', type=str, required=True, help='Path to the extracted prediction markdown file')
    parser.add_argument('--gt_path', type=str, required=True, help='Path to the ground truth markdown file')
    parser.add_argument('--result', type=str, required=True, help='Path to save the result in jsonl format')

    args = parser.parse_args()

    # 计算提取准确度
    accuracy = evaluate_extraction(pred_path=args.pred_path, gt_path=args.gt_path)

    # 保存结果
    result = {
        "Process": True,
        "Results": accuracy >= 0.95,
        "TimePoint": os.popen('date +"%Y-%m-%dT%H:%M:%S"').read().strip(),
        "comments": f"字符级准确率: {accuracy:.4f} {'满足' if accuracy >= 0.95 else '不满足'} 95% 精度要求"
    }

    # 如果文件存在，追加写入，否则创建新文件
    if os.path.exists(args.result):
        with open(args.result, 'a', encoding='utf-8') as f:
            f.write(f"{str(result)}\n")
    else:
        with open(args.result, 'w', encoding='utf-8') as f:
            f.write(f"{str(result)}\n")

    print(f"结果已保存到: {args.result}")

if __name__ == "__main__":
    main()
