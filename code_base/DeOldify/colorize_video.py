
from deoldify import device
from deoldify.device_id import DeviceId

# Force CPU mode
device.set(device=DeviceId.CPU)
print("Warning: Running in CPU-only mode - performance will be reduced")

from deoldify.visualize import get_video_colorizer
import warnings
warnings.filterwarnings('ignore', category=UserWarning, message='.*?Your .*? set is empty.*?')

# Initialize the colorizer with minimal dependencies
colorizer = get_video_colorizer(render_factor=21)
input_path = '/data/data/agent_test_codebase/GitTaskBench/queries/DeOldify_03/input/DeOldify_03_input.mp4'
output_path = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/DeOldify_03/output.mp4'

# Run the video colorization
colorizer.colorize_from_file_name(input_path, output_path, render_factor=21)

print(f'Video colorization complete: {output_path}')