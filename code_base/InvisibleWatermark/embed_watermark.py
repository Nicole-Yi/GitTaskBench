
from PIL import Image
import numpy as np
from imwatermark import WatermarkEncoder
import os

# Input image path
input_image_path = '/data/data/agent_test_codebase/GitTaskBench/queries/InvisibleWatermark_03/input/InvisibleWatermark_03_input.png'

# Output directory path
output_directory = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/InvisibleWatermark_03'

# Check if output directory exists, if not create one
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Output image path
output_image_path = os.path.join(output_directory, 'output.png')

# Read the input image
img = Image.open(input_image_path)
bgr = np.array(img)

# Define the watermark
watermark = 'watermark'

# Initialize the WatermarkEncoder
encoder = WatermarkEncoder()
encoder.set_watermark('bytes', watermark.encode('utf-8'))

# Embed the watermark
bgr_encoded = encoder.encode(bgr, 'dwtDct')

# Save the encoded image
Image.fromarray(bgr_encoded).save(output_image_path)