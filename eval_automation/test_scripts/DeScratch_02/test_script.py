import os
import argparse
import cv2
import numpy as np
import json
from datetime import datetime

def load_images(pred_dir, gt_dir):
    pred_path = os.path.join(pred_dir, "output.png")
    gt_path = os.path.join(gt_dir, "gt.png")

    if not os.path.exists(pred_path) or not os.path.exists(gt_path):
        return None, None

    pred_img = cv2.imread(pred_path)
    gt_img = cv2.imread(gt_path)

    if pred_img is None or gt_img is None:
        return None, None

    # 确保图像尺寸一致
    pred_img = cv2.resize(pred_img, (gt_img.shape[1], gt_img.shape[0]))
    return pred_img, gt_img

def compute_metrics(pred_img, gt_img):
    # 计算均方误差 (MSE)
    mse_val = np.mean((pred_img - gt_img) ** 2)

    # 计算平均绝对误差 (MAE)
    mae_val = np.mean(np.abs(pred_img - gt_img))

    return mse_val, mae_val

def evaluate_quality(pred_dir, gt_dir, threshold_mse=100, threshold_mae=15, result_file=None):
    result = {
        "Process": True,
        "Result": False, 
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

    pred_img, gt_img = load_images(pred_dir, gt_dir)
    if pred_img is None or gt_img is None:
        result["Process"] = False
        result["comments"] = "预测图像或GT图像缺失或读取失败"
        print("⚠️ 图像缺失或读取失败")
        save_result(result_file, result)
        return

    # 计算质量指标
    mse_val, mae_val = compute_metrics(pred_img, gt_img)

    print(f"均方误差（MSE）：{mse_val:.4f}")
    print(f"平均绝对误差（MAE）：{mae_val:.2f}")

    # 评估结果
    if mse_val <= threshold_mse and mae_val <= threshold_mae:
        result["Result"] = True
        result["comments"] = f"测试通过，MSE={mse_val:.4f}, MAE={mae_val:.2f}"
        print("✅ 恢复效果达标")
    else:
        result["Result"] = False
        result["comments"] = f"测试未通过，MSE={mse_val:.4f}, MAE={mae_val:.2f}"
        print("❌ 恢复效果未达标")

    save_result(result_file, result)

def save_result(result_file, result):
    if result_file:
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(result_file) or '.', exist_ok=True)
            
            # 确保写入时使用 utf-8 编码，避免中文字符被转义为 Unicode 编码
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
