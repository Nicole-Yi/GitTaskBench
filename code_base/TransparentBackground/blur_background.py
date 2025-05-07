
import os
import numpy as np
import imageio
from transparent_background.Remover import Remover

# Input and Output paths
input_image_path = '/data/data/agent_test_codebase/GitTaskBench/queries/TransparentBackground_03/input/TransparentBackground_03_input.jpg'
output_directory = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/TransparentBackground_03'
output_image_path = os.path.join(output_directory, 'output.jpg')

# Create output directory if not exists
os.makedirs(output_directory, exist_ok=True)

# Load input image using imageio
img = imageio.imread(input_image_path)

# Convert image to numpy array
img = np.array(img, dtype=np.uint8)

# Initialize Remover
remover = Remover()

# Process image to blur the background
blurred_img = remover.process(img, type='blur')

# Save output image using imageio
imageio.imwrite(output_image_path, blurred_img)

print(f'Blurred image saved to {output_image_path}')