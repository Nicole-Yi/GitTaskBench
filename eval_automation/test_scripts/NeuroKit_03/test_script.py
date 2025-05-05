import pandas as pd
import numpy as np
import json
import argparse
import os
from datetime import datetime

# 自定义 JSON 序列化函数
def custom_json_serializer(obj):
    if isinstance(obj, (bool, np.bool_)):  # 支持原生 Python bool 和 numpy.bool_
        return bool(obj)  # 确保返回原生布尔值
    raise TypeError(f"Type {type(obj)} not serializable")

def evaluate_rsp_metrics(output_csv, ground_truth_csv, result_file="results.jsonl"):
    """
    评估 RSP 信号分析结果与 ground truth 的效果。

    参数:
        output_csv (str): 包含预测指标的 CSV 文件路径
        ground_truth_csv (str): 包含 ground truth 指标的 CSV 文件路径
        result_file (str): 评估结果保存的 JSONL 文件路径

    返回:
        dict: 包含评估指标和成功状态
    """
    result = {
        "Process": False,  # 默认值为 False，表示没有通过初步检查
        "Result": False,  # 默认值为 False，表示未通过所有指标
        "TimePoint": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),  # 当前时间
        "comments": ""  # 默认没有评论
    }

    # 验证输入文件
    if not os.path.exists(output_csv):
        result["comments"] = f"Error: Output CSV file '{output_csv}' does not exist"
        print(result["comments"])
        save_result(result_file, result)
        return result
    if not os.path.exists(ground_truth_csv):
        result["comments"] = f"Error: Ground truth CSV file '{ground_truth_csv}' does not exist"
        print(result["comments"])
        save_result(result_file, result)
        return result
    if os.path.getsize(output_csv) == 0:
        result["comments"] = f"Error: Output CSV file '{output_csv}' is empty"
        print(result["comments"])
        save_result(result_file, result)
        return result
    if os.path.getsize(ground_truth_csv) == 0:
        result["comments"] = f"Error: Ground truth CSV file '{ground_truth_csv}' is empty"
        print(result["comments"])
        save_result(result_file, result)
        return result

    # 加载 CSV 文件
    try:
        output_df = pd.read_csv(output_csv)
        gt_df = pd.read_csv(ground_truth_csv)
    except Exception as e:
        result["comments"] = f"Error loading CSV files: {e}"
        print(result["comments"])
        save_result(result_file, result)
        return result

    # 验证必要列
    required_columns = ["Mean_Respiratory_Rate_BPM", "Number_of_Peaks", "Peak_Times_Seconds"]
    for df, name in [(output_df, "Output"), (gt_df, "Ground Truth")]:
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            result["comments"] = f"Error: {name} CSV missing columns: {missing_cols}"
            print(result["comments"])
            save_result(result_file, result)
            return result

    # 提取指标
    pred_rate = output_df["Mean_Respiratory_Rate_BPM"].iloc[0]
    pred_peaks = json.loads(output_df["Peak_Times_Seconds"].iloc[0])
    pred_count = output_df["Number_of_Peaks"].iloc[0]

    gt_rate = gt_df["Mean_Respiratory_Rate_BPM"].iloc[0]
    gt_peaks = json.loads(gt_df["Peak_Times_Seconds"].iloc[0])
    gt_count = gt_df["Number_of_Peaks"].iloc[0]

    # 评估指标
    result["comments"] = f"Evaluation results: MAE = {abs(pred_rate - gt_rate):.2f}, Peak Matching Rate = {sum(1 for p in pred_peaks if p in gt_peaks)/len(pred_peaks):.2f}"

    # 1. 呼吸率 MAE
    rate_mae = abs(pred_rate - gt_rate) if not np.isnan(pred_rate) and not np.isnan(gt_rate) else np.nan
    rate_success = rate_mae <= 1.0 if not np.isnan(rate_mae) else False

    # 2. 峰值时间匹配
    peak_matching_rate = sum(1 for p in pred_peaks if p in gt_peaks) / len(pred_peaks) if pred_peaks else 0.0
    peak_success = peak_matching_rate >= 0.8

    # 3. 峰值数量误差
    peak_count_relative_error = abs(pred_count - gt_count) / gt_count if gt_count > 0 else np.nan
    count_success = peak_count_relative_error <= 0.1 if not np.isnan(peak_count_relative_error) else False

    # 结果判定
    result["Result"] = rate_success and peak_success and count_success
    result["Process"] = True  # 只要文件验证通过，Process为True

    # 打印结果
    print(f"Evaluation Result: {result['Result']}")
    print(f"Comments: {result['comments']}")

    # 保存到文件时使用自定义的 JSON 序列化函数
    save_result(result_file, result)

    return result

def save_result(result_file, result):
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(result_file) or '.', exist_ok=True)

        # 检查文件是否为空，如果为空则写入 JSONL 文件头
        file_mode = "a" if os.path.exists(result_file) and os.path.getsize(result_file) > 0 else "w"
        
        with open(result_file, file_mode, encoding='utf-8') as f:
            # 写入 JSON 对象，并加上换行符
            f.write(json.dumps(result, ensure_ascii=False, default=custom_json_serializer) + "\n")
        
        print(f"[成功] 输出文件: {result_file}")
    except Exception as e:
        print(f"⚠️ 写入结果文件失败：{e}")

def main():
    parser = argparse.ArgumentParser(description="Evaluate RSP metrics against ground truth")
    parser.add_argument("--output_csv", required=True, help="Path to output CSV file (rsp_metrics.csv)")
    parser.add_argument("--ground_truth_csv", required=True, help="Path to ground truth CSV file")
    parser.add_argument("--result", default="results.jsonl", help="Path to JSONL result file")
    args = parser.parse_args()

    result = evaluate_rsp_metrics(args.output_csv, args.ground_truth_csv, args.result)
    if not result:
        print("Evaluation failed due to invalid input")

if __name__ == "__main__":
    main()
