
from PIL import Image
from imwatermark import WatermarkDecoder
import numpy as np

# Load the image 
image_path = '/data/data/agent_test_codebase/GitTaskBench/queries/InvisibleWatermark_02/input/InvisibleWatermark_02_input.png'
image = Image.open(image_path)

# Convert the image to RGB if not already, and then to a numpy array
if image.mode != 'RGB':
    image = image.convert('RGB')
bgr = np.array(image)

# Initialize the decoder
decoder = WatermarkDecoder('bytes', 32)

# Decode the watermark
watermark = decoder.decode(bgr, 'dwtDct')

# Output the decoded watermark
print(watermark.decode('utf-8'))