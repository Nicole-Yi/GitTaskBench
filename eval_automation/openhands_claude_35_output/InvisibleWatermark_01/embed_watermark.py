import sys
import numpy as np
from PIL import Image
sys.path.append('/data/data/agent_test_codebase/GitTaskBench/code_base/InvisibleWatermark')
from imwatermark import WatermarkEncoder

# 读取输入图像
input_path = '/data/data/agent_test_codebase/GitTaskBench/queries/InvisibleWatermark_01/input/LeInvisibleWatermark_01_input.png'
output_path = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/InvisibleWatermark_01/output.png'

# 读取图像
img = Image.open(input_path)
# 转换为BGR格式的numpy数组
img_array = np.array(img)
if len(img_array.shape) == 2:  # 如果是灰度图
    img_array = np.stack([img_array] * 3, axis=-1)
elif img_array.shape[2] == 4:  # 如果是RGBA图
    img_array = img_array[:, :, :3]
bgr = img_array[:, :, ::-1]  # RGB转BGR

# 创建水印编码器
encoder = WatermarkEncoder()
# 设置水印内容（这里使用一个示例水印文本）
wm = 'OpenHands'
encoder.set_watermark('bytes', wm.encode('utf-8'))

# 编码水印
bgr_encoded = encoder.encode(bgr, 'dwtDct')

# 转换回RGB并保存
rgb_encoded = bgr_encoded[:, :, ::-1]  # BGR转RGB
img_encoded = Image.fromarray(rgb_encoded)
img_encoded.save(output_path)
print(f"Watermark embedded successfully. Output saved to: {output_path}")