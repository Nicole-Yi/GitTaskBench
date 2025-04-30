import argparse
from stegano import lsb
import cv2
from skimage.metrics import peak_signal_noise_ratio as compare_psnr

def evaluate_watermark(input_path, watermark, output_path):
    # === 1. 提取水印 ===
    extracted = lsb.reveal(output_path)
    match = (extracted == watermark)
    print(f"{':white_check_mark:' if match else ':x:'} 提取结果: '{extracted}' | GT: '{watermark}'")

    # === 2. 计算 PSNR ===
    original_img = cv2.imread(input_path)
    watermarked_img = cv2.imread(output_path)

    if original_img.shape != watermarked_img.shape:
        raise ValueError("图像尺寸不一致，无法比较PSNR")

    psnr = compare_psnr(original_img, watermarked_img)
    print(f":triangular_ruler: PSNR: {psnr:.2f} dB")

    # === 3. 评估结果 ===
    print("\n:dart: 评估指标：")
    print(f" - 水印检测_match: {'100%' if match else '0%'}")
    print(f" - PSNR ≥ 40.0: {':white_check_mark: 满足' if psnr >= 40.0 else ':x: 不满足'}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="提取并评估64位水印的准确性与PSNR")
    parser.add_argument("--input", required=True, help="原始图像路径")
    parser.add_argument("--watermark", required=True, help="期望提取的64位水印（8字符）")
    parser.add_argument("--output", required=True, help="嵌入水印后的图像路径")

    args = parser.parse_args()
    evaluate_watermark(args.input, args.watermark, args.output) 