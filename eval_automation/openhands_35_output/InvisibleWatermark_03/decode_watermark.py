import cv2
import numpy as np
import pywt

def decode_watermark(img, watermark_length):
    # 将图像转换为YUV颜色空间
    yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    y = yuv[:,:,0]
    
    # 对Y通道进行小波变换
    coeffs = pywt.dwt2(y, 'haar')
    cA, (cH, cV, cD) = coeffs
    
    # 从小波系数中提取水印
    watermark_bits = []
    n = 0
    for i in range(watermark_length * 8):  # 每个字符8位
        if n >= cA.size:
            break
        row = n // cA.shape[1]
        col = n % cA.shape[1]
        bit = 1 if cA[row, col] > 0 else 0
        watermark_bits.append(bit)
        n += 1
    
    # 将二进制转换回文本
    watermark_bytes = []
    for i in range(0, len(watermark_bits), 8):
        byte = watermark_bits[i:i+8]
        if len(byte) == 8:
            char_code = int(''.join(str(b) for b in byte), 2)
            watermark_bytes.append(char_code)
    
    watermark = bytes(watermark_bytes).decode('utf-8', errors='ignore')
    return watermark

# 读取水印图像
watermarked_path = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/InvisibleWatermark_03/output.png'
img = cv2.imread(watermarked_path)

# 解码水印
watermark = decode_watermark(img, len('watermark'))
print(f"解码的水印: {watermark}")