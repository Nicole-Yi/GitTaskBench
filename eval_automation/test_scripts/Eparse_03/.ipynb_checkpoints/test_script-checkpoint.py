import argparse
import json
import os
import datetime
import Levenshtein

def compute_similarity(pred_text, gt_text):
    """计算字符级相似度，基于Levenshtein距离"""
    levenshtein_distance = Levenshtein.distance(pred_text, gt_text)
    similarity = 1 - levenshtein_distance / max(len(pred_text), len(gt_text))
    return similarity

def is_valid_file(file_path):
    """判断文件是否存在且非空"""
    return os.path.isfile(file_path) and os.path.getsize(file_path) > 0

def evaluate(pred_file, gt_file):
    """读取文件并计算相似度"""
    try:
        with open(pred_file, 'r', encoding='utf-8') as f_pred:
            pred_text = f_pred.read()
        with open(gt_file, 'r', encoding='utf-8') as f_gt:
            gt_text = f_gt.read()
    except Exception as e:
        return None, f"❌ 文件读取错误: {str(e)}"

    similarity = compute_similarity(pred_text, gt_text)
    return similarity, f"✅ 相似度计算完成: {similarity:.4f}"

def save_result(result_path, data):
    """保存结果到jsonl文件"""
    os.makedirs(os.path.dirname(result_path), exist_ok=True)
    with open(result_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False, default=str) + "\n")

def main():
    parser = argparse.ArgumentParser(description="Compare similarity between predicted and ground truth texts.")
    parser.add_argument('--pred', required=True, help="Path to predicted text file.")
    parser.add_argument('--gt', required=True, help="Path to ground truth text file.")
    parser.add_argument('--result', required=True, help="Path to save evaluation results (.jsonl).")
    args = parser.parse_args()

    result_dict = {
        "Process": False,
        "Result": False,
        "TimePoint": datetime.datetime.now().isoformat(),
        "comments": ""
    }

    # Step 1: 检查文件是否存在且非空
    if not is_valid_file(args.pred):
        result_dict["comments"] = "❌ 预测文件不存在或为空"
        save_result(args.result, result_dict)
        print(result_dict["comments"])
        return

    if not is_valid_file(args.gt):
        result_dict["comments"] = "❌ GT文件不存在或为空"
        save_result(args.result, result_dict)
        print(result_dict["comments"])
        return

    result_dict["Process"] = True

    # Step 2: 评估相似度
    similarity, msg = evaluate(args.pred, args.gt)
    if similarity is None:
        result_dict["comments"] = msg
        save_result(args.result, result_dict)
        print(msg)
        return

    result_dict["comments"] = msg
    result_dict["Result"] = similarity >= 0.8
    save_result(args.result, result_dict)

    print(msg)
    if result_dict["Result"]:
        print("✅ Passed: 相似度大于等于 0.8")
    else:
        print("❌ Failed: 相似度低于 0.8")

if __name__ == "__main__":
    main()
