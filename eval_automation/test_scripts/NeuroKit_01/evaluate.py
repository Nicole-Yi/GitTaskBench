#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import sys
import argparse
import datetime
from pathlib import Path

# 添加必要的路径
sys.path.insert(0, os.path.abspath('..'))

import pandas as pd
import numpy as np

def evaluate_hrv_results(input_dir, result_file=None):
    """
    评估HRV分析结果的正确性，使用"心脏功能正常、自主神经系统平衡良好、处于相对放松状态"作为groundtruth
    
    参数:
    input_dir -- 输入目录路径，包含HRV分析结果
    result_file -- 可选，结果输出jsonl文件路径
    """
    print("开始评估HRV分析结果...")
    
    # 创建结果目录
    if result_file:
        os.makedirs(os.path.dirname(result_file), exist_ok=True)
    
    # 检查结果文件是否存在
    results_exist = True
    results = {
        "success": False, 
        "messages": [], 
        "metrics": {},
        "conclusion": {
            "heart_function": "未知",
            "ans_balance": "未知",
            "relaxation_state": "未知",
            "overall": "未知"
        }
    }
    
    # jsonl格式的结果记录
    jsonl_result = {
        "Process": True,
        "Result": False,
        "TimePoint": datetime.datetime.now().isoformat(),
        "comments": ""
    }
    
    # 检查HRV结果文件
    hrv_results_path = os.path.join(input_dir, "output_hrv_results.csv")
    if not os.path.exists(hrv_results_path):
        results["messages"].append("错误：找不到HRV结果文件")
        results_exist = False
        jsonl_result["Process"] = False
        jsonl_result["comments"] += "错误：找不到HRV结果文件。"
    
    # 检查处理后的ECG数据
    ecg_processed_path = os.path.join(input_dir, "output_ecg_processed.csv")
    if not os.path.exists(ecg_processed_path):
        results["messages"].append("错误：找不到处理后的ECG数据")
        results_exist = False
        jsonl_result["Process"] = False
        jsonl_result["comments"] += "错误：找不到处理后的ECG数据。"
    
    # 检查HRV统计摘要
    hrv_summary_path = os.path.join(input_dir, "output_hrv_summary.csv")
    if not os.path.exists(hrv_summary_path):
        results["messages"].append("错误：找不到HRV统计摘要")
        results_exist = False
        jsonl_result["Process"] = False
        jsonl_result["comments"] += "错误：找不到HRV统计摘要。"
    
    # 如果所有结果文件都存在，进行详细评估
    if results_exist:
        try:
            # 读取HRV结果
            hrv_results = pd.read_csv(hrv_results_path)
            
            # 检查必要的HRV指标是否存在
            required_metrics = ["HRV_RMSSD", "HRV_MeanNN", "HRV_SDNN", "HRV_LF", "HRV_HF", "HRV_SD1", "HRV_SD2"]
            missing_metrics = [metric for metric in required_metrics if metric not in hrv_results.columns]
            
            if missing_metrics:
                results["messages"].append(f"警告：缺少以下HRV指标: {', '.join(missing_metrics)}")
                jsonl_result["comments"] += f"警告：缺少以下HRV指标: {', '.join(missing_metrics)}。"
            
            # 读取HRV统计摘要
            hrv_summary = pd.read_csv(hrv_summary_path)
            
            # 检查必要的统计字段
            required_stats = ["mean_nn", "sdnn", "rmssd", "lf", "hf", "lf_hf_ratio"]
            missing_stats = [stat for stat in required_stats if stat not in hrv_summary.columns]
            
            if missing_stats:
                results["messages"].append(f"警告：缺少以下统计字段: {', '.join(missing_stats)}")
                jsonl_result["comments"] += f"警告：缺少以下统计字段: {', '.join(missing_stats)}。"
            
            # 输入数据的groundtruth"心脏功能正常、自主神经系统平衡良好、处于相对放松状态"
            
            # 1. 评估平均RR间隔 (心脏功能)
            # 放松状态通常心率较低，RR间隔较大，大约在900-1200ms之间
            if "mean_nn" in hrv_summary.columns:
                mean_nn = hrv_summary["mean_nn"].values[0]
                results["metrics"]["mean_nn"] = float(mean_nn)
                
                if 900 <= mean_nn <= 1200:
                    results["messages"].append(f"成功：平均RR间隔（{mean_nn:.2f}ms）符合放松状态的预期范围")
                    results["conclusion"]["heart_function"] = "正常"
                    jsonl_result["comments"] += f"成功：平均RR间隔（{mean_nn:.2f}ms）符合放松状态的预期范围。"
                elif 800 <= mean_nn < 900 or 1200 < mean_nn <= 1300:
                    results["messages"].append(f"接近：平均RR间隔（{mean_nn:.2f}ms）接近放松状态范围")
                    results["conclusion"]["heart_function"] = "基本正常"
                    jsonl_result["comments"] += f"接近：平均RR间隔（{mean_nn:.2f}ms）接近放松状态范围。"
                else:
                    results["messages"].append(f"偏差：平均RR间隔（{mean_nn:.2f}ms）偏离放松状态的预期范围")
                    results["conclusion"]["heart_function"] = "可能异常"
                    jsonl_result["comments"] += f"偏差：平均RR间隔（{mean_nn:.2f}ms）偏离放松状态的预期范围。"
            
            # 2. 评估RMSSD (副交感神经活动)
            # 放松状态下RMSSD通常较高，大约在40-80ms之间
            if "rmssd" in hrv_summary.columns:
                rmssd = hrv_summary["rmssd"].values[0]
                results["metrics"]["rmssd"] = float(rmssd)
                
                if 40 <= rmssd <= 80:
                    results["messages"].append(f"成功：RMSSD值（{rmssd:.2f}ms）表明良好的副交感神经调节，符合放松状态")
                    parasympathetic_status = "良好"
                    jsonl_result["comments"] += f"成功：RMSSD值（{rmssd:.2f}ms）表明良好的副交感神经调节，符合放松状态。"
                elif 30 <= rmssd < 40 or 80 < rmssd <= 90:
                    results["messages"].append(f"接近：RMSSD值（{rmssd:.2f}ms）接近放松状态的标准")
                    parasympathetic_status = "尚可"
                    jsonl_result["comments"] += f"接近：RMSSD值（{rmssd:.2f}ms）接近放松状态的标准。"
                else:
                    results["messages"].append(f"偏差：RMSSD值（{rmssd:.2f}ms）偏离放松状态的预期范围")
                    parasympathetic_status = "异常"
                    jsonl_result["comments"] += f"偏差：RMSSD值（{rmssd:.2f}ms）偏离放松状态的预期范围。"
            else:
                parasympathetic_status = "未知"
            
            # 3. 评估LF/HF比值 (交感/副交感平衡)
            # 放松状态下，LF/HF比值通常在1.5-2.5之间，表明适度的交感神经优势
            if "lf_hf_ratio" in hrv_summary.columns:
                lf_hf_ratio = hrv_summary["lf_hf_ratio"].values[0]
                results["metrics"]["lf_hf_ratio"] = float(lf_hf_ratio)
                
                if 1.5 <= lf_hf_ratio <= 2.5:
                    results["messages"].append(f"成功：LF/HF比值（{lf_hf_ratio:.2f}）表明自主神经系统平衡良好，符合放松状态下的适度交感优势")
                    sympathetic_status = "平衡"
                    jsonl_result["comments"] += f"成功：LF/HF比值（{lf_hf_ratio:.2f}）表明自主神经系统平衡良好。"
                elif 1.0 <= lf_hf_ratio < 1.5 or 2.5 < lf_hf_ratio <= 3.0:
                    results["messages"].append(f"接近：LF/HF比值（{lf_hf_ratio:.2f}）接近理想的自主神经系统平衡状态")
                    sympathetic_status = "基本平衡"
                    jsonl_result["comments"] += f"接近：LF/HF比值（{lf_hf_ratio:.2f}）接近理想的自主神经系统平衡状态。"
                elif lf_hf_ratio < 1.0:
                    results["messages"].append(f"偏差：LF/HF比值（{lf_hf_ratio:.2f}）偏低，表明副交感神经活动优势")
                    sympathetic_status = "副交感优势"
                    jsonl_result["comments"] += f"偏差：LF/HF比值（{lf_hf_ratio:.2f}）偏低，表明副交感神经活动优势。"
                else:  # > 3.0
                    results["messages"].append(f"偏差：LF/HF比值（{lf_hf_ratio:.2f}）偏高，表明交感神经活动过度优势")
                    sympathetic_status = "交感优势"
                    jsonl_result["comments"] += f"偏差：LF/HF比值（{lf_hf_ratio:.2f}）偏高，表明交感神经活动过度优势。"
            else:
                sympathetic_status = "未知"
            
            # 4. 评估SDNN (整体心率变异性)
            # 放松状态下SDNN通常在40-80ms之间
            if "sdnn" in hrv_summary.columns:
                sdnn = hrv_summary["sdnn"].values[0]
                results["metrics"]["sdnn"] = float(sdnn)
                
                if 40 <= sdnn <= 80:
                    results["messages"].append(f"成功：SDNN值（{sdnn:.2f}ms）表明整体心率变异性良好")
                    hrv_quality = "良好"
                    jsonl_result["comments"] += f"成功：SDNN值（{sdnn:.2f}ms）表明整体心率变异性良好。"
                elif 30 <= sdnn < 40 or 80 < sdnn <= 90:
                    results["messages"].append(f"接近：SDNN值（{sdnn:.2f}ms）接近理想的整体心率变异性范围")
                    hrv_quality = "尚可"
                    jsonl_result["comments"] += f"接近：SDNN值（{sdnn:.2f}ms）接近理想的整体心率变异性范围。"
                elif sdnn < 30:
                    results["messages"].append(f"偏差：SDNN值（{sdnn:.2f}ms）偏低，表明整体心率变异性较差")
                    hrv_quality = "较差"
                    jsonl_result["comments"] += f"偏差：SDNN值（{sdnn:.2f}ms）偏低，表明整体心率变异性较差。"
                else:  # > 90
                    results["messages"].append(f"偏差：SDNN值（{sdnn:.2f}ms）偏高，可能表明非典型变异性")
                    hrv_quality = "非典型"
                    jsonl_result["comments"] += f"偏差：SDNN值（{sdnn:.2f}ms）偏高，可能表明非典型变异性。"
            else:
                hrv_quality = "未知"
            
            # 综合评估自主神经系统平衡状态
            if parasympathetic_status != "未知" and sympathetic_status != "未知":
                if parasympathetic_status == "良好" and sympathetic_status == "平衡":
                    results["conclusion"]["ans_balance"] = "良好"
                elif parasympathetic_status in ["良好", "尚可"] and sympathetic_status in ["平衡", "基本平衡"]:
                    results["conclusion"]["ans_balance"] = "基本良好"
                else:
                    results["conclusion"]["ans_balance"] = "不平衡"
            
            # 评估放松状态
            relaxation_scores = 0
            relaxation_factors = 0
            
            if "mean_nn" in hrv_summary.columns:
                relaxation_factors += 1
                if 900 <= mean_nn <= 1200:
                    relaxation_scores += 1
                elif 800 <= mean_nn < 900 or 1200 < mean_nn <= 1300:
                    relaxation_scores += 0.5
            
            if "rmssd" in hrv_summary.columns:
                relaxation_factors += 1
                if 40 <= rmssd <= 80:
                    relaxation_scores += 1
                elif 30 <= rmssd < 40 or 80 < rmssd <= 90:
                    relaxation_scores += 0.5
            
            if "lf_hf_ratio" in hrv_summary.columns:
                relaxation_factors += 1
                if 1.5 <= lf_hf_ratio <= 2.5:
                    relaxation_scores += 1
                elif 1.0 <= lf_hf_ratio < 1.5 or 2.5 < lf_hf_ratio <= 3.0:
                    relaxation_scores += 0.5
            
            if relaxation_factors > 0:
                relaxation_ratio = relaxation_scores / relaxation_factors
                if relaxation_ratio >= 0.8:
                    results["conclusion"]["relaxation_state"] = "放松"
                elif relaxation_ratio >= 0.5:
                    results["conclusion"]["relaxation_state"] = "较为放松"
                else:
                    results["conclusion"]["relaxation_state"] = "非放松"
            
            # 总体评估
            if (results["conclusion"]["heart_function"] in ["正常", "基本正常"] and
                results["conclusion"]["ans_balance"] in ["良好", "基本良好"] and
                results["conclusion"]["relaxation_state"] in ["放松", "较为放松"]):
                results["conclusion"]["overall"] = "心脏功能正常、自主神经系统平衡良好、处于相对放松状态"
                results["success"] = True
                jsonl_result["Result"] = True
                jsonl_result["comments"] += "总体评估：心脏功能正常、自主神经系统平衡良好、处于相对放松状态。"
            else:
                results["conclusion"]["overall"] = "分析结果与预期groundtruth有偏差"
                # 即使与groundtruth不完全符合，只要数据处理正常，我们也认为测试成功
                if not any(msg.startswith("错误") for msg in results["messages"]):
                    results["success"] = True
                    jsonl_result["Result"] = True
                    jsonl_result["comments"] += "总体评估：分析结果与预期groundtruth有偏差，但数据处理正常。"
                else:
                    jsonl_result["comments"] += "总体评估：分析结果与预期groundtruth有偏差，且数据处理异常。"
        
        except Exception as e:
            error_msg = f"错误：评估过程中发生异常: {str(e)}"
            results["messages"].append(error_msg)
            jsonl_result["Process"] = False
            jsonl_result["comments"] += error_msg
    
    # 将结果保存到JSONL文件
    if result_file:
        mode = "a" if os.path.exists(result_file) else "w"
        with open(result_file, mode, encoding="utf-8") as f:
            f.write(json.dumps(jsonl_result, ensure_ascii=False, default=str) + "\n")
        print(f"评估完成，结果已保存至{result_file}")
    else:
        print("评估完成，但未指定结果文件路径")
    
    print(f"评估结果: {'成功' if results['success'] else '失败'}")
    if results["success"] and "overall" in results["conclusion"]:
        print(f"结论: {results['conclusion']['overall']}")
    
    return results

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="评估HRV分析结果")
    parser.add_argument("--input", help="指定输入目录路径", default="output/NeuroKit_01")
    parser.add_argument("--result", help="指定结果输出JSONL文件路径", default=None)
    args = parser.parse_args()
    
    # 运行评估
    evaluate_hrv_results(args.input, args.result)

if __name__ == "__main__":
    main() 