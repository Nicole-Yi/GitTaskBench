#!/usr/bin/env python3
import os
import sys
import argparse
import cv2                             # pip install opencv-python
import numpy as np
import json
from datetime import datetime
from skimage.metrics import (
    peak_signal_noise_ratio,          # PSNR
    structural_similarity             # SSIM
)

def check_file(path, exts=('.png', '.jpg', '.jpeg', '.webp')):
    if not os.path.isfile(path):
        sys.exit(f"错误：文件不存在 -> {path}")
    if not path.lower().endswith(exts):
        sys.exit(f"错误：不支持的格式 -> {path}")

def load_and_prepare(path, target_shape=None):
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    if img is None:
        sys.exit(f"错误：无法读取图像 -> {path}")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if target_shape and img.shape[:2] != target_shape:
        img = cv2.resize(img, (target_shape[1], target_shape[0]),
                         interpolation=cv2.INTER_LINEAR)
    return img

def save_result_jsonl(process, results, comments, result_file):
    """
    将单条记录以 JSONL 格式追加到文件
    """
    record = {
        "Process": bool(process),
        "Result": bool(results),
        "TimePoint": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "comments": comments
    }
    # 确保目录存在
    os.makedirs(os.path.dirname(result_file), exist_ok=True)
    # 追加写入一行 JSONL
    with open(result_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False, default=str))
        f.write("\n")

def main():
    p = argparse.ArgumentParser(
        description="评估重建图像与参考图像的 PSNR/SSIM，并动态适配 win_size，输出 JSONL 格式结果"
    )
    p.add_argument('ref', help="参考图像路径")
    p.add_argument('sr',  help="重建/超分图像路径")
    p.add_argument('--psnr-thresh', type=float, default=18.0,
                   help="PSNR 阈值 (dB)")
    p.add_argument('--ssim-thresh', type=float, default=0.80,
                   help="SSIM 阈值")
    p.add_argument('--result', required=True,
                   help="输出 JSONL 文件路径")
    args = p.parse_args()

    process = os.path.exists(args.sr)
    if not process:
        comments = f"预测文件不存在：{args.sr}"
        save_result_jsonl(process, False, comments, args.result)
        print(False)
        sys.exit(0)

    try:
        # 1. 文件合法性检测
        check_file(args.ref)
        check_file(args.sr)

        # 2. 读取参考图像得到目标尺寸
        ref0 = cv2.imread(args.ref, cv2.IMREAD_COLOR)
        H, W = ref0.shape[:2]

        # 3. 加载并可能 Resize
        ref = load_and_prepare(args.ref, (H, W))
        sr  = load_and_prepare(args.sr,  (H, W))

        # 4. 计算 PSNR
        psnr_val = peak_signal_noise_ratio(ref, sr, data_range=255)

        # 5. 动态计算 SSIM 窗口大小
        win = min(H, W)
        if win % 2 == 0:
            win -= 1
        win = max(win, 1)

        # 6. 计算 SSIM
        ssim_val = structural_similarity(
            ref, sr,
            channel_axis=-1,
            win_size=win,
            data_range=255
        )

        # 7. 判定结果
        results = (psnr_val >= args.psnr_thresh) and (ssim_val >= args.ssim_thresh)
        comments = (
            f"PSNR: {psnr_val:.2f} dB (阈值: {args.psnr_thresh}), "
            f"SSIM: {ssim_val:.4f} (阈值: {args.ssim_thresh}, win_size={win})"
        )

        save_result_jsonl(process, results, comments, args.result)
        print(results)

    except Exception as e:
        save_result_jsonl(process, False, str(e), args.result)
        print(False)
        sys.exit(1)

if __name__ == "__main__":
    main()