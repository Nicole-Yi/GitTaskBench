import cv2
import os
from imwatermark import WatermarkDecoder

# Set paths
input_image_path = '/data/data/agent_test_codebase/GitTaskBench/queries/InvisibleWatermark_02/input/InvisibleWatermark_02_input.png'
output_dir = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/InvisibleWatermark_02'
output_file_path = os.path.join(output_dir, 'output')

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Read the image
bgr = cv2.imread(input_image_path)

# Create a decoder for 4 characters (32 bits)
decoder = WatermarkDecoder('bytes', 32)

# Try different methods to decode the watermark
methods = ['dwtDct', 'dwtDctSvd', 'rivaGan']
results = {}

for method in methods:
    try:
        print(f"Trying to decode with method: {method}")
        watermark = decoder.decode(bgr, method)
        decoded_text = watermark.decode('utf-8')
        print(f"Decoded watermark with {method}: {decoded_text}")
        results[method] = decoded_text
    except Exception as e:
        print(f"Error decoding with {method}: {e}")
        results[method] = f"Error: {str(e)}"

# Write the results to the output file
with open(output_file_path, 'w') as f:
    if results:
        # If we have successful results, use the first successful one
        for method, result in results.items():
            if not result.startswith("Error"):
                f.write(result)
                print(f"Successfully decoded watermark: {result}")
                break
        else:
            # If all methods failed, write the errors
            f.write("Failed to decode watermark with all methods:\n")
            for method, error in results.items():
                f.write(f"{method}: {error}\n")
    else:
        f.write("Failed to decode watermark")

print(f"Results written to {output_file_path}")