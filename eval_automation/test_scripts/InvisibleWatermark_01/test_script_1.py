import argparse
import cv2
from imwatermark import WatermarkDecoder
from skimage.metrics import peak_signal_noise_ratio as compare_psnr

def evaluate_watermark(original_path, watermark_text, watermarked_path):
    bgr_original = cv2.imread(original_path)
    bgr_encoded = cv2.imread(watermarked_path)

    if bgr_original is None or bgr_encoded is None:
        raise FileNotFoundError("读取图像失败，请确认路径是否正确")

    # 提取水印
    decoder = WatermarkDecoder('bytes', len(watermark_text) * 8)
    decoded_bytes = decoder.decode(bgr_encoded, 'dwtDct')
    extracted_text = decoded_bytes.decode('utf-8', errors='ignore')

    # 比对
    is_match = (extracted_text == watermark_text)
    print(f"{':white_check_mark:' if is_match else ':x:'} 提取结果: '{extracted_text}' | GT: '{watermark_text}'")

    # PSNR
    psnr_value = compare_psnr(bgr_original, bgr_encoded)
    print(f":triangular_ruler: PSNR: {psnr_value:.2f} dB")

    # 输出指标
    print("\n:dart: 评估指标：")
    print(f" - 水印检测_match: {'100%' if is_match else '0%'}")
    print(f" - PSNR ≥ 40.0: {':white_check_mark: 满足' if psnr_value >= 40.0 else ':x: 不满足'}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="提取并验证盲水印，计算图像质量")
    parser.add_argument("--input", required=True, help="原始图像路径")
    parser.add_argument("--output", required=True, help="嵌入水印后的图像路径")
    parser.add_argument("--watermark", required=True, help="期望提取的水印内容")

    args = parser.parse_args()
    evaluate_watermark(args.input,  args.watermark, args.output) 