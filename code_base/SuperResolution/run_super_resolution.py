
import os
import numpy as np
from skimage.io import imread, imsave
from ISR.models.rrdn import RRDN

# Load input image
input_path = '/data/data/agent_test_codebase/GitTaskBench/queries/SuperResolution_02/input/SuperResolution_02_input.jpg'
output_dir = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/SuperResolution_02'
os.makedirs(output_dir, exist_ok=True)
input_image = imread(input_path)

# Initialize RRDN model
rrdn = RRDN(arch_params={'C': 4, 'D': 3, 'G': 32, 'G0': 32, 'T': 10, 'x': 4}, weights='gans')
weights_path = rrdn.weights_url['gans']['rrdn']  # Path to weights file
rrdn.model.load_weights(weights_path)

# Predict high resolution image
predict_image = rrdn.predict(input_image)

# Save output image
output_path = os.path.join(output_dir, 'output.jpg')
imsave(output_path, predict_image)

print(f'Super-resolution completed. Output saved at {output_path}')