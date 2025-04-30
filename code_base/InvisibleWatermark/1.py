import cv2
from imwatermark import WatermarkEncoder
import argparse


input_path = '/mnt/nfs_200T/home/nzy/GitTaskBench/queries/InvisibleWatermark_01/input/InvisibleWatermark_01_input.png'

watermark_text = 'invisible'

output_path = '/mnt/nfs_200T/home/nzy/GitTaskBench/eval_automation/output/InvisibleWatermark_01/output.png'

bgr = cv2.imread(input_path)
if bgr is None:
    raise FileNotFoundError(f"无法读取图像：{input_path}")

encoder = WatermarkEncoder()
encoder.set_watermark('bytes', watermark_text.encode('utf-8'))
bgr_encoded = encoder.encode(bgr, 'dwtDct')

cv2.imwrite(output_path, bgr_encoded)
print(f"✅ 水印已嵌入并保存至：{output_path}")

