import pandas as pd
import numpy as np
import json
import argparse
import os
from datetime import datetime

def evaluate_rsp_metrics(output_csv, ground_truth_csv, result_file="evaluation_results.jsonl"):
    """
    评估 RSP 信号分析结果与 ground truth 的效果。

    参数:
        output_csv (str): 包含预测指标的 CSV 文件路径（Mean_Respiratory_Rate_BPM, Peak_Times_Seconds, Number_of_Peaks）
        ground_truth_csv (str): 包含 ground truth 指标的 CSV 文件路径
        result_file (str): 评估结果保存的 JSONL 文件路径

    返回:
        dict: 包含评估指标和成功状态
    """
    # 验证输入文件
    if not os.path.exists(output_csv):
        print(f"Error: Output CSV file '{output_csv}' does not exist")
        return {}
    if not os.path.exists(ground_truth_csv):
        print(f"Error: Ground truth CSV file '{ground_truth_csv}' does not exist")
        return {}
    if os.path.getsize(output_csv) == 0:
        print(f"Error: Output CSV file '{output_csv}' is empty")
        return {}
    if os.path.getsize(ground_truth_csv) == 0:
        print(f"Error: Ground truth CSV file '{ground_truth_csv}' is empty")
        return {}

    # 加载 CSV 文件
    try:
        output_df = pd.read_csv(output_csv)
        gt_df = pd.read_csv(ground_truth_csv)
    except Exception as e:
        print(f"Error loading CSV files: {e}")
        return {}

    # 验证必要列
    required_columns = ["Mean_Respiratory_Rate_BPM", "Number_of_Peaks", "Peak_Times_Seconds"]
    for df, name in [(output_df, "Output"), (gt_df, "Ground Truth")]:
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            print(f"Error: {name} CSV missing columns: {missing_cols}")
            return {}

    # 提取指标
    pred_rate = output_df["Mean_Respiratory_Rate_BPM"].iloc[0]
    pred_peaks = json.loads(output_df["Peak_Times_Seconds"].iloc[0])
    pred_count = output_df["Number_of_Peaks"].iloc[0]

    gt_rate = gt_df["Mean_Respiratory_Rate_BPM"].iloc[0]
    gt_peaks = json.loads(gt_df["Peak_Times_Seconds"].iloc[0])
    gt_count = gt_df["Number_of_Peaks"].iloc[0]

    # 评估指标
    result = {
        "output_csv": output_csv,
        "ground_truth_csv": ground_truth_csv,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # 1. 呼吸率 MAE
    rate_mae = abs(pred_rate - gt_rate) if not np.isnan(pred_rate) and not np.isnan(gt_rate) else np.nan
    result["rate_mae"] = float(rate_mae) if not np.isnan(rate_mae) else None
    rate_success = rate_mae <= 1.0 if not np.isnan(rate_mae) else False

    # 2. 峰值时间 MPTD 和匹配率
    if pred_peaks and gt_peaks:
        peak_errors = [min(abs(p - gt) for gt in gt_peaks) for p in pred_peaks]
        peak_mptd = sum(peak_errors) / len(peak_errors) if peak_errors else np.nan
        peak_matching_count = sum(1 for err in peak_errors if err <= 0.1)
        peak_matching_rate = peak_matching_count / len(pred_peaks) if pred_peaks else 0.0
    else:
        peak_mptd = np.nan
        peak_matching_rate = 0.0
    result["peak_mptd"] = float(peak_mptd) if not np.isnan(peak_mptd) else None
    result["peak_matching_rate"] = float(peak_matching_rate)
    peak_success = (peak_mptd <= 0.1 and peak_matching_rate >= 0.8) if not np.isnan(peak_mptd) else False

    # 3. 峰值数量相对误差
    peak_count_relative_error = (
        abs(pred_count - gt_count) / gt_count if gt_count > 0 else np.nan
    )
    result["peak_count_relative_error"] = float(peak_count_relative_error) if not np.isnan(peak_count_relative_error) else None
    count_success = peak_count_relative_error <= 0.1 if not np.isnan(peak_count_relative_error) else False

    # 判断任务成功（转换为字符串以确保 JSON 序列化）
    result["success"] = str(rate_success and peak_success and count_success).lower()

    # 打印结果
    print("Evaluation Results:")
    print(f"Rate MAE: {rate_mae:.2f} BPM (Success: {rate_mae <= 1.0})")
    print(f"Peak MPTD: {peak_mptd:.3f} seconds (Success: {peak_mptd <= 0.1})")
    print(f"Peak Matching Rate: {peak_matching_rate:.2f} (Success: {peak_matching_rate >= 0.8})")
    print(f"Peak Count Relative Error: {peak_count_relative_error:.2f} (Success: {peak_count_relative_error <= 0.1})")
    print(f"Overall Success: {result['success'] == 'true'}")

    # 保存结果到 JSONL
    with open(result_file, "a") as f:
        json.dump(result, f)
        f.write("\n")

    return result

def main():
    parser = argparse.ArgumentParser(description="Evaluate RSP metrics against ground truth")
    parser.add_argument("--output_csv", required=True, help="Path to output CSV file (rsp_metrics.csv)")
    parser.add_argument("--ground_truth_csv", required=True, help="Path to ground truth CSV file")
    parser.add_argument("--result", default="evaluation_results.jsonl", help="Path to JSONL result file")
    args = parser.parse_args()

    result = evaluate_rsp_metrics(args.output_csv, args.ground_truth_csv, args.result)
    if not result:
        print("Evaluation failed due to invalid input")

if __name__ == "__main__":
    main()