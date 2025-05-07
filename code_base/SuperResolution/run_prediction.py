
import numpy as np
import matplotlib.pyplot as plt
from ISR.models import RRDN

# Load the image from file
input_path = '/data/data/agent_test_codebase/GitTaskBench/queries/SuperResolution_03/input/SuperResolution_03_input.png'
output_path = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/SuperResolution_03/output.png'

image = plt.imread(input_path)

# Initialize the model with GAN weights
model = RRDN(weights='gans')

# Super-resolve the image by model predict method
sr_image = model.predict(image)

# Save the output to file
plt.imsave(output_path, sr_image)