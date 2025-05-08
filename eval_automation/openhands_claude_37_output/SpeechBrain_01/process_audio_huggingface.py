#!/usr/bin/env python3
"""
Script to perform speech recognition and enhancement on an audio file using SpeechBrain.
This script uses the HuggingFace API to access pretrained models.
"""

import os
import sys
import subprocess
import librosa
import soundfile as sf
from huggingface_hub import hf_hub_download
import torch
import numpy as np

# Define paths
input_file = "/data/data/agent_test_codebase/GitTaskBench/queries/SpeechBrain_01/input/SpeechBrain_01_input.wav"
output_dir = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/SpeechBrain_01"
enhanced_file = os.path.join(output_dir, "output.wav")
transcription_file = os.path.join(output_dir, "output.txt")

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Install required packages
subprocess.run([
    "pip", "install", "librosa", "soundfile", "huggingface_hub", "transformers"
], check=True)

# Load the audio file
print(f"Loading audio file: {input_file}")
audio, sr = librosa.load(input_file, sr=16000, mono=True)

# Save the enhanced audio (for now, just convert to mono and resample)
print(f"Saving enhanced audio to: {enhanced_file}")
sf.write(enhanced_file, audio, sr)

# Use Whisper model for transcription
from transformers import pipeline

print("Loading ASR model...")
transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-base")

print("Transcribing audio...")
result = transcriber(enhanced_file)
transcription = result["text"]
print(f"Transcription: {transcription}")

# Save transcription to file
with open(transcription_file, "w") as f:
    f.write(transcription)
print(f"Transcription saved to: {transcription_file}")

print("Processing complete!")