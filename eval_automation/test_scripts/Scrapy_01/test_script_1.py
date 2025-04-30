import argparse
import json
import os
import datetime


def evaluate_scrapy_output(pred_path: str, truth_path: str, result_path: str = "test_results/Scrapy_01/scrapy_results.json") -> bool:
    """
    比较 Scrapy 抓取结果与 ground truth 的字段级准确率（Field-level Accuracy）。

    参数：
        pred_path: 抓取结果的 JSONL 文件路径
        truth_path: 标注的 ground truth JSONL 文件路径
        result_path: 结果保存的 JSON 文件路径

    返回：
        是否提取有效（布尔值）
    """
    threshold = 0.95  # 定义是否"提取有效"的阈值

    if not os.path.exists(pred_path) or not os.path.exists(truth_path):
        raise FileNotFoundError("输入文件路径无效！")

    with open(pred_path, "r", encoding="utf-8") as f_pred, \
         open(truth_path, "r", encoding="utf-8") as f_true:
        pred_lines = [json.loads(line.strip()) for line in f_pred if line.strip()]
        true_lines = [json.loads(line.strip()) for line in f_true if line.strip()]

    if len(pred_lines) != len(true_lines):
        print("警告: 抓取结果与标注样本数量不一致（预测 {0} 条，真实 {1} 条）".format(len(pred_lines), len(true_lines)))

    total_fields = 0
    correct_fields = 0

    for pred, true in zip(pred_lines, true_lines):
        for field in ["author", "text"]:
            total_fields += 1
            if pred.get(field, "").strip() == true.get(field, "").strip():
                correct_fields += 1

    accuracy = correct_fields / total_fields if total_fields else 0
    result = accuracy >= threshold
    
    # 保存结果到 JSON 文件
    save_result(result, result_path)
    
    # 只输出 True 或 False
    print(str(result).lower())
    
    return result


def save_result(result: bool, result_path: str):
    """保存测试结果到 JSON 文件"""
    # 确保目录存在
    os.makedirs(os.path.dirname(result_path), exist_ok=True)
    
    # 准备新结果
    new_result = {
        "Results": result,
        "TimePoint": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    }
    
    # 读取现有结果或创建新文件
    results = []
    if os.path.exists(result_path):
        try:
            with open(result_path, "r", encoding="utf-8") as f:
                results = json.load(f)
                if not isinstance(results, list):
                    results = [results]
        except json.JSONDecodeError:
            results = []
    
    # 添加新结果并保存
    results.append(new_result)
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="评估 Scrapy 抓取结果的字段级准确率")
    parser.add_argument("--pred_file", type=str, required=True, help="预测结果（JSONL）路径")
    parser.add_argument("--truth_file", type=str, required=True, help="标注数据（JSONL）路径")
    parser.add_argument("--result_file", type=str, default="test_results/Scrapy_01/scrapy_results.json", help="结果保存路径")

    args = parser.parse_args()
    evaluate_scrapy_output(args.pred_file, args.truth_file, args.result_file) 