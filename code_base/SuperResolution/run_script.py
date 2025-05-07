
import numpy as np
import cv2
from ISR.models import RRDN

input_path = '/data/data/agent_test_codebase/GitTaskBench/queries/SuperResolution_03/input/SuperResolution_03_input.png'
output_path = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/SuperResolution_03/output.png'

# Load image with cv2
image = cv2.imread(input_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

model = RRDN(weights='gans')
sr_image = model.predict(image)

cv2.imwrite(output_path, cv2.cvtColor(sr_image, cv2.COLOR_RGB2BGR))