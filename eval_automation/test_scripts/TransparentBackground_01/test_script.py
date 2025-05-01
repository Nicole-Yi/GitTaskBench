#!/usr/bin/env python3
import sys
import argparse
import cv2   # pip install opencv-python
import numpy as np   # pip install numpy
import json
import os
from datetime import datetime

def image_colorfulness(image):
    """
    计算图像色彩丰富度:
    Hasler & Süsstrunk (2003) 定义的公式
    """
    # 如果图像是4通道（BGRA），只取BGR三个通道
    if image.shape[-1] == 4:
        image = image[:, :, :3]
    
    # 确保图像是3通道的
    if len(image.shape) != 3 or image.shape[-1] != 3:
        raise ValueError("输入图像必须是3通道(BGR)或4通道(BGRA)格式")
    
    (B, G, R) = cv2.split(image.astype("float"))
    rg = np.abs(R - G)
    yb = np.abs(0.5 * (R + G) - B)
    rbMean, rbStd = np.mean(rg), np.std(rg)
    ybMean, ybStd = np.mean(yb), np.std(yb)
    return np.sqrt(rbStd**2 + ybStd**2) + 0.3 * np.sqrt(rbMean**2 + ybMean**2)

def save_result(result, reason, process, result_file):
    """
    保存测试结果到JSON文件
    """
    # 准备新的结果数据，确保 result 是 JSON 可序列化的布尔值
    new_result = {
        "Process": bool(process),  # 处理状态放在最前面
        "Results": bool(result),
        "TimePoint": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "Reason": reason
    }
    
    # 读取现有数据（如果存在）
    existing_results = []
    if os.path.exists(result_file):
        with open(result_file, 'r', encoding='utf-8') as f:
            try:
                existing_results = json.load(f)
                if not isinstance(existing_results, list):
                    existing_results = [existing_results]
            except json.JSONDecodeError:
                existing_results = []
    
    # 添加新结果
    existing_results.append(new_result)
    
    # 保存更新后的结果
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(existing_results, f, ensure_ascii=False, indent=2)

def main():
    parser = argparse.ArgumentParser(
        description="评估抠图前后图像色彩丰富度差值，并据 threshold 判定是否通过"
    )
    parser.add_argument('orig', help="原始图像路径 (支持 .jpg/.png)")
    parser.add_argument('pred', help="抠图结果图像路径 (支持 .png)")
    parser.add_argument(
        '--colorfulness-diff-thresh', type=float, default=20.0,
        help="色彩丰富度差值阈值：orig - pred ≥ thresh 时判定通过"
    )
    parser.add_argument('--result', help="结果文件路径")
    args = parser.parse_args()

    # 检查预测文件是否存在
    process = os.path.exists(args.pred)
    
    # 如果预测文件不存在，直接返回结果
    if not process:
        reason = f"预测文件不存在：{args.pred}"
        save_result(False, reason, process)
        print(False)
        sys.exit(0)

    # 加载图像
    orig = cv2.imread(args.orig, cv2.IMREAD_UNCHANGED)
    pred = cv2.imread(args.pred, cv2.IMREAD_UNCHANGED)
    if orig is None:
        reason = f"错误：无法加载原图 {args.orig}"
        save_result(False, reason, process)
        print(False)
        sys.exit(0)
    if pred is None:
        reason = f"错误：无法加载结果图 {args.pred}"
        save_result(False, reason, process)
        print(False)
        sys.exit(0)

    # 计算色彩丰富度
    cf_orig = image_colorfulness(orig)
    cf_pred = image_colorfulness(pred)
    diff = cf_orig - cf_pred

    # 判定结果
    result = diff >= args.colorfulness_diff_thresh
    
    # 生成原因说明
    reason = (
        f"原图色彩丰富度: {cf_orig:.2f}, "
        f"结果图色彩丰富度: {cf_pred:.2f}, "
        f"差值: {diff:.2f}, "
        f"阈值: {args.colorfulness_diff_thresh}"
    )
    
    # 保存结果
    save_result(result, reason, process, args.result)
    
    # 只输出布尔值
    print(result)

if __name__ == "__main__":
    main()