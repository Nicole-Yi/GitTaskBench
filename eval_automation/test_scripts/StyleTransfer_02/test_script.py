import cv2
import numpy as np
from skimage.metrics import peak_signal_noise_ratio as psnr
import argparse
import json
import os
from datetime import datetime

def evaluate_reconstruction(input_img_path, output_img_path):
    """
    使用PSNR评估重建效果。

    参数：
    - input_img_path: 原始内容图像的路径
    - output_img_path: 重建图像的路径

    返回：
    - psnr_value: 原始图像与重建图像的PSNR值
    - result: 任务完成情况 ("成功" 或 "失败")
    """
    # 加载原始图像和重建图像
    original_img = cv2.imread(input_img_path)
    original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)  # 转为RGB格式
    reconstructed_img = cv2.imread(output_img_path)
    reconstructed_img = cv2.cvtColor(reconstructed_img, cv2.COLOR_BGR2RGB)  # 转为RGB格式

    # 调整图像大小以确保两者尺寸一致
    if original_img.shape != reconstructed_img.shape:
        reconstructed_img = cv2.resize(reconstructed_img, (original_img.shape[1], original_img.shape[0]))

    # 计算PSNR（峰值信噪比）
    psnr_value = psnr(original_img, reconstructed_img)

    # 判断任务是否成功（成功：PSNR > 30）
    if psnr_value > 10:
        result = "成功"
    else:
        result = "失败"

    return psnr_value, result

def evaluate_task(input_img_path, output_img_path, result_path=None):
    """
    评估任务并将结果保存到指定文件。

    参数：
    - input_img_path: 原始内容图像路径
    - output_img_path: 任务输出的重建图像路径
    - result_path: 结果保存的路径
    """
    psnr_value, result = evaluate_reconstruction(input_img_path, output_img_path)

    # 打印评估结果
    print(f"\n评估结果：")
    print(f"------------------------------")
    print(f"PSNR（峰值信噪比）: {psnr_value:.2f} dB")
    print(f"任务结果: {result}")
    print(f"------------------------------")

    # 将结果保存到 JSONL 文件
    if result_path:
        time_point = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        process_result = os.path.exists(input_img_path) and os.path.exists(output_img_path)
        results = {
            "Process": process_result,
            "Results": result == "成功",  # 如果结果是"成功"，则为 True
            "TimePoint": time_point,
            "comments": f"PSNR: {psnr_value:.2f}, 任务结果: {result}"
        }

        # 以追加的方式保存结果
        with open(result_path, 'a') as f:
            f.write(json.dumps(results, default=str) + "\n")

    return psnr_value, result


if __name__ == "__main__":
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="评估图像重建任务")
    parser.add_argument('--input_img_path', type=str, required=True, help="原始内容图像路径")
    parser.add_argument('--output_img_path', type=str, required=True, help="重建图像路径")
    parser.add_argument('--result', type=str, required=True, help="结果保存的 JSONL 文件路径")
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 调用评估任务
    evaluate_task(args.input_img_path, args.output_img_path, args.result)
