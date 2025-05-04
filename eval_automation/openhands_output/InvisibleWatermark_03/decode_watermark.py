#!/usr/bin/env python3
import sys
import os
import cv2
import numpy as np

# Add the repository to the Python path
sys.path.append('/data/data/agent_test_codebase/GitTaskBench/code_base/InvisibleWatermark')

# Import the watermark modules
from imwatermark import WatermarkDecoder

def decode_watermark(image_path, watermark_length=72):  # Default length for "watermark" (9 chars * 8 bits)
    """
    Decode a watermark from an image.
    
    Args:
        image_path (str): Path to the watermarked image
        watermark_length (int): Length of the watermark in bits
        
    Returns:
        str: The decoded watermark text
    """
    # Read the watermarked image
    bgr = cv2.imread(image_path)
    if bgr is None:
        print(f"Error: Could not read image from {image_path}")
        return None
    
    # Create a watermark decoder
    decoder = WatermarkDecoder('bytes', watermark_length)
    
    # Decode the watermark
    watermark = decoder.decode(bgr, 'dwtDct')
    
    # Convert the watermark bytes to text
    try:
        decoded_text = watermark.decode('utf-8')
        return decoded_text
    except UnicodeDecodeError:
        print("Error: Could not decode watermark as UTF-8 text")
        return None

if __name__ == "__main__":
    # Use the provided image path or default to the output.png in the current directory
    image_path = sys.argv[1] if len(sys.argv) > 1 else "output.png"
    
    # Decode the watermark
    decoded_text = decode_watermark(image_path)
    
    if decoded_text:
        print(f"Decoded watermark: {decoded_text}")
    else:
        print("Failed to decode watermark")