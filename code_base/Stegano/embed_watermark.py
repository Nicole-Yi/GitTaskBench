import os
from PIL import Image

def hide_message(image_path, message, output_path):
    """Minimal LSB implementation without external dependencies"""
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size
    
    binary_msg = ''.join(format(ord(c), '08b') for c in message)
    binary_msg += '00000000'  # Null terminator
    
    if len(binary_msg) > width * height * 3:
        raise ValueError("Message too long for image capacity")
    
    index = 0
    for y in range(height):
        for x in range(width):
            pixel = list(pixels[x, y])
            for color in range(3):  # R,G,B
                if index < len(binary_msg):
                    pixel[color] = pixel[color] & ~1 | int(binary_msg[index])
                    index += 1
            pixels[x, y] = tuple(pixel)
    
    img.save(output_path)

# Input and output paths
input_image = "/data/data/agent_test_codebase/GitTaskBench/queries/Stegano_01/input/Stegano_01_input.png"
output_dir = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Stegano_01"
watermark = "stegano"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Embed watermark
try:
    output_path = os.path.join(output_dir, "output.png")
    hide_message(input_image, watermark, output_path)
    print(f"Watermark embedded successfully. Output saved to {output_path}")
except Exception as e:
    print(f"Error embedding watermark: {str(e)}")