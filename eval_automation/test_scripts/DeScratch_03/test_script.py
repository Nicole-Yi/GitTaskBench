import os
import argparse
import cv2
import numpy as np
import json
from datetime import datetime
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim

def evaluate_quality(pred_dir, gt_dir, threshold_ssim=0.65, threshold_psnr=15, result_file=None):
    result = {
        "Process": True,
        "Results": False,
        "TimePoint": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "comments": ""
    }

    print(f"\n开始评估任务：")
    print(f"预测图像路径：{pred_dir}")
    print(f"真实图像路径：{gt_dir}\n")

    if not os.path.exists(pred_dir) or not os.path.exists(gt_dir):
        result["Process"] = False
        result["comments"] = "路径不存在"
        print("❌ 路径不存在")
        save_result(result_file, result)
        return

    pred_path = os.path.join(pred_dir, "output.png")
    gt_path = os.path.join(gt_dir, "gt.png")

    if not os.path.exists(pred_path) or not os.path.exists(gt_path):
        result["Process"] = False
        result["comments"] = "预测图像或GT图像缺失"
        print(f"⚠️ 缺失图像：{'output.png' if not os.path.exists(pred_path) else ''} {'gt.png' if not os.path.exists(gt_path) else ''}")
        save_result(result_file, result)
        return

    pred_img = cv2.imread(pred_path)
    gt_img = cv2.imread(gt_path)

    if pred_img is None or gt_img is None:
        result["Process"] = False
        result["comments"] = "图像读取失败"
        print("⚠️ 图像读取失败")
        save_result(result_file, result)
        return

    pred_img = cv2.resize(pred_img, (gt_img.shape[1], gt_img.shape[0]))
    pred_gray = cv2.cvtColor(pred_img, cv2.COLOR_BGR2GRAY)
    gt_gray = cv2.cvtColor(gt_img, cv2.COLOR_BGR2GRAY)

    ssim_val = ssim(gt_gray, pred_gray)
    psnr_val = psnr(gt_gray, pred_gray)

    print(f"平均结构相似性（SSIM）：{ssim_val:.4f}")
    print(f"平均峰值信噪比（PSNR）：{psnr_val:.2f}")

    if ssim_val >= threshold_ssim and psnr_val >= threshold_psnr:
        result["Results"] = True
        result["comments"] = f"测试通过，SSIM={ssim_val:.4f}, PSNR={psnr_val:.2f}"
        print("✅ 恢复效果达标")
    else:
        result["Results"] = False
        result["comments"] = f"测试未通过，SSIM={ssim_val:.4f}, PSNR={psnr_val:.2f}"
        print("❌ 恢复效果未达标")

    save_result(result_file, result)

def save_result(result_file, result):
    if result_file:
        try:
            with open(result_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(result, ensure_ascii=False) + "\n")
            print(f"[成功] 输出文件: {result_file}")
        except Exception as e:
            print(f"⚠️ 写入结果文件失败：{e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--pred_dir', type=str, required=True, help='预测结果文件夹')
    parser.add_argument('--gt_dir', type=str, required=True, help='原始GT文件夹')
    parser.add_argument('--result', type=str, required=True, help='结果输出JSONL文件')
    args = parser.parse_args()

    evaluate_quality(args.pred_dir, args.gt_dir, result_file=args.result)
