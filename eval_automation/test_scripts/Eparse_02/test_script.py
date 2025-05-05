import argparse
import json
import os
from datetime import datetime

def load_text(file_path):
    """读取文本文件，返回标准化的字符串"""
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    return ''.join(text.split()).lower()  # 去除空白符，只比核心内容

def evaluate(pred_path, gt_path):
    """按字符级别评估"""
    threshold = 0.80  # 固定阈值

    pred_text = load_text(pred_path)
    gt_text = load_text(gt_path)

    # 结果字典初始化
    result = {
        "Process": True,
        "Result": False,  # 统一使用单数形式
        "TimePoint": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "comments": ""
    }

    # 检查输入文件是否有效
    if not pred_text or not gt_text:
        result["Process"] = False
        result["comments"] = "输入文件为空，无法进行评估！"
        return result

    if not gt_text:
        result["comments"] = "❌ ground truth为空！"
        result["Result"] = False
        return result

    # 计算字符级准确率
    common_len = sum((1 for c1, c2 in zip(pred_text, gt_text) if c1 == c2))
    total_len = len(gt_text)

    accuracy = common_len / total_len if total_len else 0

    # 根据准确率判断结果
    if accuracy >= threshold:
        result["Result"] = True  # 统一使用单数形式
        result["comments"] = f"✅ 测试通过！字符级Accuracy={accuracy:.4f} ≥ {threshold}"
    else:
        result["Result"] = False  # 统一使用单数形式
        result["comments"] = f"❌ 测试未通过。字符级Accuracy={accuracy:.4f} < {threshold}"

    return result

def save_result(result, result_file):
    """保存结果到 jsonl 文件"""
    # 确保目录存在
    os.makedirs(os.path.dirname(result_file) or '.', exist_ok=True)
    
    # 追加模式写入，确保每条记录单独一行
    with open(result_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(result, ensure_ascii=False) + "\n")

def main():
    parser = argparse.ArgumentParser(description="Evaluate output by text similarity and save results")
    parser.add_argument("--pred", required=True, help="Predicted output file path")
    parser.add_argument("--gt", required=True, help="Ground truth file path")
    parser.add_argument("--result", required=True, help="Result output file path (JSONL format)")
    args = parser.parse_args()

    # 获取评估结果
    result = evaluate(args.pred, args.gt)

    # 将结果保存到指定的 jsonl 文件
    save_result(result, args.result)
    print(f"结果已保存到 {args.result}")

if __name__ == "__main__":
    main()