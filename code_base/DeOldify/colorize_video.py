
from deoldify import device
from deoldify.device_id import DeviceId

# Set the device to GPU
# If you want to use the CPU, set device=DeviceId.CPU
# Note: Running on CPU might be significantly slower than on GPU

device.set(device=DeviceId.GPU0)

from deoldify.visualize import *
import warnings
warnings.filterwarnings('ignore', category=UserWarning, message='.*?Your .*? set is empty.*?')

# Initialize the colorizer
colorizer = get_video_colorizer()
input_path = '/data/data/agent_test_codebase/GitTaskBench/queries/DeOldify_03/input/DeOldify_03_input.mp4'
output_path = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/DeOldify_03/output.mp4'

# Run the video colorization
colorizer.colorize_from_file_name(input_path, output_path, render_factor=21)

print(f'Video colorization complete: {output_path}')