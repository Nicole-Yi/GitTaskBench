import cv2
from imwatermark import WatermarkDecoder

# 读取带水印的图像
input_path = '/data/data/agent_test_codebase/GitTaskBench/queries/InvisibleWatermark_02/input/InvisibleWatermark_02_input.png'
bgr = cv2.imread(input_path)

# 创建解码器，设置类型为bytes，长度为32（4字符 * 8位/字符）
decoder = WatermarkDecoder('bytes', 32)

# 使用默认的dwtDct方法解码
watermark = decoder.decode(bgr, 'dwtDct')

# 将bytes解码为utf-8字符串
result = watermark.decode('utf-8')
print(f"Decoded watermark: {result}")

# 将结果保存到输出文件
output_path = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/InvisibleWatermark_02/output'
with open(output_path, 'w') as f:
    f.write(result)