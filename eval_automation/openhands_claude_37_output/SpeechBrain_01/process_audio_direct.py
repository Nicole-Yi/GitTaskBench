#!/usr/bin/env python3
"""
Script to perform speech recognition and enhancement on an audio file using SpeechBrain.
This script uses the SpeechBrain repository directly.
"""

import os
import sys
import subprocess

# Define paths
input_file = "/data/data/agent_test_codebase/GitTaskBench/queries/SpeechBrain_01/input/SpeechBrain_01_input.wav"
output_dir = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/SpeechBrain_01"
enhanced_file = os.path.join(output_dir, "output.wav")
transcription_file = os.path.join(output_dir, "output.txt")

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Create a temporary Python script for enhancement
enhancement_script = os.path.join(output_dir, "enhance.py")
with open(enhancement_script, "w") as f:
    f.write("""
import os
import sys
import torch
import torchaudio
from speechbrain.inference.enhancement import SpectralMaskEnhancement

# Define paths
input_file = sys.argv[1]
output_file = sys.argv[2]

# Enhance the audio using MetricGAN+ model
print("Loading speech enhancement model...")
enhancer = SpectralMaskEnhancement.from_hparams(
    source="speechbrain/metricgan-plus-voicebank",
    savedir="pretrained_models/metricgan-plus-voicebank"
)

print(f"Enhancing audio file: {input_file}")
enhanced = enhancer.enhance_file(input_file, output_filename=output_file)
print(f"Enhanced audio saved to: {output_file}")
""")

# Create a temporary Python script for ASR
asr_script = os.path.join(output_dir, "transcribe.py")
with open(asr_script, "w") as f:
    f.write("""
import os
import sys
import torch
import torchaudio
from speechbrain.inference.ASR import EncoderDecoderASR

# Define paths
input_file = sys.argv[1]
output_file = sys.argv[2]

# Perform speech recognition
print("Loading ASR model...")
asr_model = EncoderDecoderASR.from_hparams(
    source="speechbrain/asr-conformer-transformerlm-librispeech",
    savedir="pretrained_models/asr-conformer-transformerlm-librispeech"
)

print("Transcribing audio...")
transcription = asr_model.transcribe_file(input_file)
print(f"Transcription: {transcription}")

# Save transcription to file
with open(output_file, "w") as f:
    f.write(transcription)
print(f"Transcription saved to: {output_file}")
""")

# Run the enhancement script
print("Running speech enhancement...")
subprocess.run([
    "python", "-m", "pip", "install", "speechbrain", "torch", "torchaudio"
], check=True)

print("Enhancing audio...")
subprocess.run([
    "python", enhancement_script, input_file, enhanced_file
], check=True)

# Run the ASR script
print("Running speech recognition...")
subprocess.run([
    "python", asr_script, enhanced_file, transcription_file
], check=True)

print("Processing complete!")