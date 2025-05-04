import cv2
import numpy as np
import pywt

def embed_watermark(img, watermark_text):
    # 将图像转换为YUV颜色空间
    yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    y = yuv[:,:,0]
    
    # 对Y通道进行小波变换
    coeffs = pywt.dwt2(y, 'haar')
    cA, (cH, cV, cD) = coeffs
    
    # 将水印文本转换为二进制
    watermark_bits = ''.join(format(ord(c), '08b') for c in watermark_text)
    watermark_bits = [int(bit) for bit in watermark_bits]
    
    # 在小波系数中嵌入水印
    n = 0
    alpha = 20  # 水印强度
    for i in range(len(watermark_bits)):
        if n >= cA.size:
            break
        row = n // cA.shape[1]
        col = n % cA.shape[1]
        if watermark_bits[i] == 1:
            cA[row, col] += alpha
        else:
            cA[row, col] -= alpha
        n += 1
    
    # 进行逆小波变换
    y_watermarked = pywt.idwt2((cA, (cH, cV, cD)), 'haar')
    
    # 确保值在合适的范围内并调整大小以匹配原始图像
    y_watermarked = np.clip(y_watermarked, 0, 255)
    if y_watermarked.shape != y.shape:
        y_watermarked = cv2.resize(y_watermarked, (y.shape[1], y.shape[0]))
    
    # 替换YUV图像中的Y通道
    yuv_watermarked = yuv.copy()
    yuv_watermarked[:,:,0] = y_watermarked
    
    # 转换回BGR颜色空间
    bgr_watermarked = cv2.cvtColor(yuv_watermarked, cv2.COLOR_YUV2BGR)
    
    return bgr_watermarked

# 读取输入图像
input_path = '/data/data/agent_test_codebase/GitTaskBench/queries/InvisibleWatermark_03/input/InvisibleWatermark_03_input.png'
output_path = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/InvisibleWatermark_03/output.png'

# 读取图像
img = cv2.imread(input_path)

# 嵌入水印
watermarked_img = embed_watermark(img, 'watermark')

# 保存结果
cv2.imwrite(output_path, watermarked_img)
print(f"水印已嵌入并保存到: {output_path}")