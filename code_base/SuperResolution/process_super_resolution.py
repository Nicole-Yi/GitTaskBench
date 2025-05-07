
import numpy as np
from PIL import Image
from ISR.models import RRDN

# Paths
input_path = '/data/data/agent_test_codebase/GitTaskBench/queries/SuperResolution_02/input/SuperResolution_02_input.jpg'
output_dir = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/SuperResolution_02'
output_path = f'{output_dir}/output.jpg'

# Load input image
input_image = np.array(Image.open(input_path))

# Initialize RRDN model
rrdn = RRDN(weights='gans')

# Super-resolution
sr_image = rrdn.predict(input_image)

# Save output image
Image.fromarray(sr_image).save(output_path)

print(f'Super-resolution completed. Output saved at {output_path}')