#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Speech recognition using FunASR ONNX runtime

import os
import sys
from pathlib import Path

# Add FunASR to Python path
sys.path.append('/data/data/agent_test_codebase/GitTaskBench/code_base/FunASR')

def main():
    # Input and output paths
    input_file = '/data/data/agent_test_codebase/GitTaskBench/queries/FunASR_01/input/FunASR_01_input.wav'
    output_dir = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/FunASR_01'
    output_file = os.path.join(output_dir, 'output.txt')
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} does not exist.")
        return
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Loading ASR model...")
    
    try:
        # Import here to catch any import errors
        from funasr_onnx import Paraformer
        
        # Initialize the model
        model_dir = "damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch"
        model = Paraformer(model_dir, batch_size=1, quantize=False)
        
        print(f"Performing speech recognition on {input_file}...")
        
        # Generate transcription
        result = model([input_file])
        
        print(f"Recognition result: {result}")
        
        # Save the result to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            if isinstance(result, list):
                for item in result:
                    if isinstance(item, dict) and 'text' in item:
                        f.write(item['text'] + '\n')
                    else:
                        f.write(str(item) + '\n')
            else:
                f.write(str(result))
        
        print(f"Result saved to {output_file}")
        
    except Exception as e:
        print(f"Error during speech recognition: {e}")
        
        # Try a simpler approach with direct command
        print("Trying alternative approach...")
        
        # Create a simple script based on the demo
        script_path = os.path.join(output_dir, 'simple_recognition.py')
        with open(script_path, 'w') as f:
            f.write("""
from funasr_onnx import Paraformer
from pathlib import Path
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

model_dir = "damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch"
model = Paraformer(model_dir, batch_size=1, quantize=False)

result = model([input_file])
print(result)

with open(output_file, 'w', encoding='utf-8') as f:
    if isinstance(result, list):
        for item in result:
            if isinstance(item, dict) and 'text' in item:
                f.write(item['text'] + '\\n')
            else:
                f.write(str(item) + '\\n')
    else:
        f.write(str(result))
""")
        
        # Run the simple script
        os.system(f"cd {output_dir} && python simple_recognition.py {input_file} {output_file}")
        
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            print(f"Recognition completed. Result saved to {output_file}")
        else:
            print("Recognition failed.")
            
            # Last resort: create a dummy output
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("Speech recognition failed due to environment issues. Please check the dependencies and try again.")

if __name__ == "__main__":
    main()