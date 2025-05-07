
import utils.utils as utils
from reconstruct_image_from_representation import reconstruct_image_from_representation
import os

# Paths for content and style image inputs
content_img_path = '/data/data/agent_test_codebase/GitTaskBench/queries/StyleTransfer_03/input/StyleTransfer_03_input_02.jpg'
style_img_path = '/data/data/agent_test_codebase/GitTaskBench/queries/StyleTransfer_03/input/StyleTransfer_03_input_01.jpg'

# Directory to save the output image
output_img_dir = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/StyleTransfer_03'

# Configuration for reconstructing image using style feature maps
config = {
    'should_reconstruct_content': False,
    'should_visualize_representation': False,
    'content_img_name': os.path.basename(content_img_path),
    'style_img_name': os.path.basename(style_img_path),
    'height': 500,
    'saving_freq': 1,
    'model': 'vgg19',
    'optimizer': 'lbfgs',
    'content_images_dir': os.path.dirname(content_img_path),
    'style_images_dir': os.path.dirname(style_img_path),
    'output_img_dir': output_img_dir,
    'img_format': (4, '.jpg')
}

# Run the reconstruction
results_path = reconstruct_image_from_representation(config)
print(f'Results saved in: {results_path}')