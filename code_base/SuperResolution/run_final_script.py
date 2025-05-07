import numpy as np
import sys
from ISR.models import RRDN

input_path = '/data/data/agent_test_codebase/GitTaskBench/queries/SuperResolution_03/input/SuperResolution_03_input.png'
output_path = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/SuperResolution_03/output.png'

# Load image data with numpy
width, height = 256, 256  # Update dimensions appropriately
image_data = np.fromfile(input_path, dtype=np.uint8)

if len(image_data) == width*height*3:
    image = image_data.reshape((height, width, 3))
else:
    print('Error: Image data length mismatch.')
    sys.exit(1)

model = RRDN(weights='gans')
sr_image = model.predict(image)

# Save enhanced image data
sr_image.tofile(output_path)
