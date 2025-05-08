import cv2
from imwatermark import WatermarkEncoder, WatermarkDecoder

# 读取输入图像
input_path = '/data/data/agent_test_codebase/GitTaskBench/queries/InvisibleWatermark_03/input/InvisibleWatermark_03_input.png'
output_path = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/InvisibleWatermark_03/output.png'

# 读取图像
bgr = cv2.imread(input_path)

# 创建水印编码器
encoder = WatermarkEncoder()
# 设置水印内容
encoder.set_watermark('bytes', 'watermark'.encode('utf-8'))

# 使用dwtDct方法嵌入水印
bgr_encoded = encoder.encode(bgr, 'dwtDct')

# 保存结果
cv2.imwrite(output_path, bgr_encoded)
print(f"水印已嵌入并保存到: {output_path}")

# 解码水印
decoder = WatermarkDecoder('bytes', len('watermark') * 8)  # 每个字符8位
watermark = decoder.decode(bgr_encoded, 'dwtDct')
print(f"解码的水印: {watermark}")