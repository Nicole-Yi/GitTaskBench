#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import traceback
from pathlib import Path

# Input and output paths
input_file = "/data/data/agent_test_codebase/GitTaskBench/queries/FunASR_01/input/FunASR_01_input.wav"
output_file = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/FunASR_01/output.txt"

try:
    # Import the necessary modules from funasr-onnx
    from funasr_onnx import Paraformer
    
    # Initialize the model
    # Using the pre-trained Chinese ASR model
    model = Paraformer("damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch")
    
    # Perform speech recognition
    result = model([input_file])
    
    # Extract the text from the result
    if result and isinstance(result, list) and len(result) > 0:
        recognized_text = result[0]["text"]
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