#!/usr/bin/env python3
import os, sys, argparse
import cv2                             # pip install opencv-python :contentReference[oaicite:7]{index=7}
import numpy as np
import json
from datetime import datetime
from skimage.metrics import (
    peak_signal_noise_ratio,          # PSNR :contentReference[oaicite:8]{index=8}
    structural_similarity             # SSIM :contentReference[oaicite:9]{index=9}
)

def check_file(path, exts=('.png','.jpg','.jpeg', '.webp')):
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
        # 等比/非等比缩放至目标
        img = cv2.resize(img, (target_shape[1], target_shape[0]),
                         interpolation=cv2.INTER_LINEAR)
    return img

def save_result(result, reason, process, result_file):
    """
    保存测试结果到JSON文件
    """
    # 准备新的结果数据
    new_result = {
        "Process": bool(process),
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
    p = argparse.ArgumentParser(
        description="评估重建图像与参考图像的 PSNR/SSIM，并动态适配 win_size"
    )
    p.add_argument('ref', help="参考图像路径")
    p.add_argument('sr',  help="重建/超分图像路径")
    p.add_argument('--psnr-thresh', type=float, default=18.0,
                   help="PSNR 阈值 (dB)")
    p.add_argument('--ssim-thresh', type=float, default=0.90,
                   help="SSIM 阈值")
    p.add_argument('--result', help="结果文件路径")
    args = p.parse_args()

    # 检查预测文件是否存在
    process = os.path.exists(args.sr)
    
    # 如果预测文件不存在，直接返回结果
    if not process:
        reason = f"预测文件不存在：{args.sr}"
        save_result(False, reason, process)
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
            channel_axis=-1,     # 明确通道轴 :contentReference[oaicite:10]{index=10}
            win_size=win,        # 动态奇数窗口
            data_range=255
        )

        # 7. 判定结果
        result = (psnr_val >= args.psnr_thresh) and (ssim_val >= args.ssim_thresh)
        
        # 生成原因说明
        reason = (
            f"PSNR: {psnr_val:.2f} dB (阈值: {args.psnr_thresh}), "
            f"SSIM: {ssim_val:.4f} (阈值: {args.ssim_thresh}, win_size={win})"
        )
        
        # 保存结果
        save_result(result, reason, process, args.result)
        
        # 只输出布尔值
        print(result)

    except Exception as e:
        # 如果处理过程中出现任何错误，记录错误并返回失败
        save_result(False, str(e), process)
        print(False)
        sys.exit(1)

if __name__ == "__main__":
    main()