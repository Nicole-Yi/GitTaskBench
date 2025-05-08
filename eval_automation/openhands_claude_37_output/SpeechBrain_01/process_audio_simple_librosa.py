#!/usr/bin/env python3
"""
Script to perform basic speech enhancement on an audio file using librosa.
"""

import os
import librosa
import librosa.effects
import soundfile as sf
import numpy as np

# Define paths
input_file = "/data/data/agent_test_codebase/GitTaskBench/queries/SpeechBrain_01/input/SpeechBrain_01_input.wav"
output_dir = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/SpeechBrain_01"
enhanced_file = os.path.join(output_dir, "output.wav")
info_file = os.path.join(output_dir, "output.txt")

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Load the audio file
print(f"Loading audio file: {input_file}")
audio, sr = librosa.load(input_file, sr=16000, mono=True)

# Apply some basic enhancement techniques
print("Applying speech enhancement...")

# 1. Noise reduction using spectral subtraction
# Convert to the frequency domain
stft = librosa.stft(audio)
magnitude, phase = librosa.magphase(stft)

# Estimate noise from a portion of the signal (assuming first 1 second is noise/silence)
noise_sample = magnitude[:, :int(sr/1024)]
noise_profile = np.mean(noise_sample, axis=1)

# Apply spectral subtraction
enhanced_magnitude = np.maximum(0, magnitude - noise_profile[:, np.newaxis] * 2)

# Convert back to time domain
enhanced_stft = enhanced_magnitude * phase
enhanced_audio = librosa.istft(enhanced_stft)

# 2. Apply normalization
enhanced_audio = librosa.util.normalize(enhanced_audio)

# 3. Apply dynamic range compression
percentile_low = np.percentile(enhanced_audio, 10)
percentile_high = np.percentile(enhanced_audio, 90)
enhanced_audio = np.clip(enhanced_audio, percentile_low, percentile_high)
enhanced_audio = librosa.util.normalize(enhanced_audio)

# Save the enhanced audio
print(f"Saving enhanced audio to: {enhanced_file}")
sf.write(enhanced_file, enhanced_audio, sr)

# Create a simple info file
with open(info_file, "w") as f:
    f.write("Audio Processing Information\n")
    f.write("===========================\n\n")
    f.write(f"Original file: {input_file}\n")
    f.write(f"Enhanced file: {enhanced_file}\n\n")
    f.write("Enhancement techniques applied:\n")
    f.write("1. Conversion to mono and resampling to 16kHz\n")
    f.write("2. Noise reduction using spectral subtraction\n")
    f.write("3. Audio normalization\n")
    f.write("4. Dynamic range compression\n\n")
    f.write("The enhanced audio should have reduced background noise and improved clarity.\n")

print(f"Information saved to: {info_file}")
print("Processing complete!")