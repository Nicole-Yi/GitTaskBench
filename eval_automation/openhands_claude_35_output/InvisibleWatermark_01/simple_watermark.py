from PIL import Image
import numpy as np

def embed_watermark(image_path, output_path, watermark_text='OpenHands'):
    # 读取图像
    img = Image.open(image_path)
    img_array = np.array(img)
    print(f"Image shape: {img_array.shape}")
    print(f"Image dtype: {img_array.dtype}")
    
    # 将水印文本转换为二进制
    watermark_bits = ''.join(format(ord(c), '08b') for c in watermark_text)
    print(f"Watermark bits: {watermark_bits}")
    print(f"Number of watermark bits: {len(watermark_bits)}")
    
    # 确保图像足够大以容纳水印
    if img_array.shape[0] * img_array.shape[1] < len(watermark_bits):
        raise ValueError("Image too small to contain watermark")
    
    # 在最低有效位嵌入水印
    bit_index = 0
    modified = False
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            if bit_index < len(watermark_bits):
                # 修改蓝色通道的最低有效位
                pixel = img_array[i, j]
                print(f"Processing pixel at ({i}, {j}): {pixel}")
                if len(img_array.shape) == 3:  # RGB图像
                    # 将最低有效位设置为水印位
                    # 使用位运算来修改最低有效位
                    if int(watermark_bits[bit_index]) == 1:
                        pixel[2] = pixel[2] | 1  # 设置最低位为1
                    else:
                        pixel[2] = pixel[2] & 254  # 设置最低位为0
                    img_array[i, j] = pixel
                    bit_index += 1
                    modified = True
                    if bit_index == 1:  # 只打印第一个修改的像素
                        print(f"Modified first pixel to: {img_array[i, j]}")
    
    if not modified:
        raise ValueError("Failed to embed watermark")
    
    # 保存结果
    result = Image.fromarray(img_array)
    result.save(output_path)
    print(f"Watermark embedded successfully. Output saved to: {output_path}")

# 执行水印嵌入
input_path = '/data/data/agent_test_codebase/GitTaskBench/queries/InvisibleWatermark_01/input/InvisibleWatermark_01_input.png'
output_path = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/InvisibleWatermark_01/output.png'
embed_watermark(input_path, output_path)