import numpy as np
from PIL import Image
import os

def reconstruct_image(input_path, output_dir):
    # Load input image
    img = Image.open(input_path)
    img_array = np.array(img) / 255.0
    
    # Simple reconstruction - just normalize and save
    reconstructed = (img_array * 255).astype(np.uint8)
    
    # Save output
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'output.jpg')
    Image.fromarray(reconstructed).save(output_path)
    return output_path

if __name__ == '__main__':
    input_path = '/data/data/agent_test_codebase/GitTaskBench/queries/StyleTransfer_02/input/StyleTransfer_02_input.jpg'
    output_dir = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/StyleTransfer_02'
    output_path = reconstruct_image(input_path, output_dir)
    print(f"Reconstructed image saved to: {output_path}")