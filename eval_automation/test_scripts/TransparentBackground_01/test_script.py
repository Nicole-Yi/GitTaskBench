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
    if image.shape[-1] == 4:
        image = image[:, :, :3]
    if len(image.shape) != 3 or image.shape[-1] != 3:
        raise ValueError("输入图像必须是3通道(BGR)或4通道(BGRA)格式")
    (B, G, R) = cv2.split(image.astype("float"))
    rg = np.abs(R - G)
    yb = np.abs(0.5 * (R + G) - B)
    rbMean, rbStd = np.mean(rg), np.std(rg)
    ybMean, ybStd = np.mean(yb), np.std(yb)
    return np.sqrt(rbStd**2 + ybStd**2) + 0.3 * np.sqrt(rbMean**2 + ybMean**2)

def save_result_jsonl(process, results, comments, result_file):
    """
    将单条记录以 JSONL 格式追加到文件，
    记录字段：Process, Results, TimePoint, comments
    """
    entry = {
        "Process": bool(process),
        "Results": bool(results),
        "TimePoint": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "comments": comments
    }
    # 确保目录存在
    os.makedirs(os.path.dirname(result_file), exist_ok=True)
    # 追加写入一行 JSONL
    with open(result_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False, default=str) + "\n")

def main():
    parser = argparse.ArgumentParser(
        description="评估抠图前后图像色彩丰富度差值，并据 threshold 判定是否通过，输出 JSONL 格式结果"
    )
    parser.add_argument('orig', help="原始图像路径 (支持 .jpg/.png)")
    parser.add_argument('pred', help="抠图结果图像路径 (支持 .png)")
    parser.add_argument(
        '--colorfulness-diff-thresh', type=float, default=20.0,
        help="色彩丰富度差值阈值：orig - pred ≥ thresh 时判定通过"
    )
    parser.add_argument('--result', required=True,
                        help="JSONL 结果文件路径")
    args = parser.parse_args()

    process = os.path.exists(args.pred)
    if not process:
        comments = f"预测文件不存在：{args.pred}"
        save_result_jsonl(process, False, comments, args.result)
        print(False)
        sys.exit(0)

    try:
        orig = cv2.imread(args.orig, cv2.IMREAD_UNCHANGED)
        pred = cv2.imread(args.pred, cv2.IMREAD_UNCHANGED)
        if orig is None:
            raise FileNotFoundError(f"无法加载原图：{args.orig}")
        if pred is None:
            raise FileNotFoundError(f"无法加载结果图：{args.pred}")

        cf_orig = image_colorfulness(orig)
        cf_pred = image_colorfulness(pred)
        diff = cf_orig - cf_pred
        results = diff >= args.colorfulness_diff_thresh

        comments = (
            f"原图色彩丰富度: {cf_orig:.2f}, "
            f"结果图色彩丰富度: {cf_pred:.2f}, "
            f"差值: {diff:.2f}, "
            f"阈值: {args.colorfulness_diff_thresh}"
        )

        save_result_jsonl(process, results, comments, args.result)
        print(results)

    except Exception as e:
        save_result_jsonl(process, False, str(e), args.result)
        print(False)
        sys.exit(1)

if __name__ == "__main__":
    main()
