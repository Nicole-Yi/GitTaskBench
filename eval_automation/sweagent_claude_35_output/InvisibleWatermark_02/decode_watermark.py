
import sys
import os
import cv2
sys.path.append('/data/data/agent_test_codebase/GitTaskBench/code_base/InvisibleWatermark')
from imwatermark.watermark import WatermarkDecoder


# Input image path
input_image = '/data/data/agent_test_codebase/GitTaskBench/queries/InvisibleWatermark_02/input/InvisibleWatermark_02_input.png'

# Output file path
output_dir = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/InvisibleWatermark_02'
output_file = os.path.join(output_dir, 'output')

# Read the image
bgr = cv2.imread(input_image)

# Create decoder for 4 characters (32 bits)
decoder = WatermarkDecoder('bytes', 32)

# Decode the watermark using dwtDct method (default method)
watermark = decoder.decode(bgr, 'dwtDct')

# Decode the watermark bytes to string
decoded_text = watermark.decode('utf-8')

# Write the result to output file
with open(output_file, 'w') as f:
    f.write(decoded_text)

print(f"Decoded watermark: {decoded_text}")
print("Result written to output file")