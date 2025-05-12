
from ISR.models import RDN
from PIL import Image
import numpy as np
import os

# File paths
input_path = '/data/data/agent_test_codebase/GitTaskBench/queries/SuperResolution_02/input/SuperResolution_02_input.jpg'
output_dir = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/SuperResolution_02'
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'output.jpg')

# Load image and convert to numpy array
img = Image.open(input_path).convert('RGB')
lr_img = np.array(img)

# Initialize model with reduced requirements
model = RDN(weights='psnr-small')

# Process in chunks if needed (memory management)
if lr_img.nbytes > 50 * 1024 * 1024:  # If >50MB
    chunks = [lr_img[i:i+512, j:j+512] for i in range(0, lr_img.shape[0], 512)
                                 for j in range(0, lr_img.shape[1], 512)]
    sr_chunks = [model.predict(chunk) for chunk in chunks]
    sr_img = np.vstack([np.hstack(sr_chunks[i:i+lr_img.shape[1]//512+1]) 
                       for i in range(0, len(sr_chunks), lr_img.shape[1]//512+1)])
else:
    sr_img = model.predict(lr_img)

# Save result
Image.fromarray(sr_img).save(output_path, quality=95)
print(f"Super-resolution completed. Output saved to {output_path}")