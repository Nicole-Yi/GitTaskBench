#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import traceback
import soundfile as sf
import numpy as np

# Input and output paths
input_file = "/data/data/agent_test_codebase/GitTaskBench/queries/FunASR_01/input/FunASR_01_input.wav"
output_file = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/FunASR_01/output.txt"

try:
    # Import the necessary modules from funasr-onnx
    from funasr_onnx import Paraformer
    
    # Load the audio file
    audio, sample_rate = sf.read(input_file)
    
    # Convert to mono if stereo
    if len(audio.shape) > 1:
        audio = audio[:, 0]
    
    # Ensure the audio is float32
    audio = audio.astype(np.float32)
    
    # Create a local model directory
    model_dir = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/FunASR_01/model"
    os.makedirs(model_dir, exist_ok=True)
    
    # Initialize the model with local path
    model = Paraformer(model_dir)
    
    # Perform speech recognition
    result = model(audio, sample_rate)
    
    # Extract the text from the result
    if result and isinstance(result, dict) and "text" in result:
        recognized_text = result["text"]
    else:
        recognized_text = "No text recognized or empty result."
    
    # Write the result to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(recognized_text)
    
    print(f"Speech recognition completed. Result saved to {output_file}")
    print(f"Recognized text: {recognized_text}")

except Exception as e:
    error_message = f"Error during speech recognition: {str(e)}\n{traceback.format_exc()}"
    print(error_message)
    
    # Write error message to output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"Error during speech recognition: {str(e)}")