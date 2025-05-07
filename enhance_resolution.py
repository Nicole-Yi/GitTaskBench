
import numpy as np
from PIL import Image
from ISR.models import RDN

# Load image
img_path = '/data/data/agent_test_codebase/GitTaskBench/queries/SuperResolution_01/input/SuperResolution_01_input.png'
lr_img = np.array(Image.open(img_path))

# Load pre-trained model
rdn = RDN(weights='psnr-large')

# Apply Super Resolution
sr_img = rdn.predict(lr_img)

# Save the output image
output_path = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/SuperResolution_01/output.png'
Image.fromarray(sr_img).save(output_path)
print("Image resolution enhancement completed and saved.")