#!/usr/bin/env python3
"""
Script to perform speech recognition and enhancement on an audio file using SpeechBrain.
"""

import os
import torch
import torchaudio
from speechbrain.inference.enhancement import SpectralMaskEnhancement
from speechbrain.inference.ASR import EncoderDecoderASR

# Define paths
input_file = "/data/data/agent_test_codebase/GitTaskBench/queries/SpeechBrain_01/input/SpeechBrain_01_input.wav"
output_dir = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/SpeechBrain_01"
enhanced_file = os.path.join(output_dir, "output_enhanced.wav")
transcription_file = os.path.join(output_dir, "output_transcription.txt")

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Step 1: Enhance the audio using MetricGAN+ model
print("Loading speech enhancement model...")
enhancer = SpectralMaskEnhancement.from_hparams(
    source="speechbrain/metricgan-plus-voicebank",
    savedir=os.path.join(output_dir, "pretrained_models", "metricgan-plus-voicebank")
)

print(f"Enhancing audio file: {input_file}")
enhanced = enhancer.enhance_file(input_file, output_filename=enhanced_file)
print(f"Enhanced audio saved to: {enhanced_file}")

# Step 2: Perform speech recognition on the enhanced audio
print("Loading ASR model...")
asr_model = EncoderDecoderASR.from_hparams(
    source="speechbrain/asr-conformer-transformerlm-librispeech",
    savedir=os.path.join(output_dir, "pretrained_models", "asr-conformer-transformerlm-librispeech")
)

print("Transcribing enhanced audio...")
transcription = asr_model.transcribe_file(enhanced_file)
print(f"Transcription: {transcription}")

# Save transcription to file
with open(transcription_file, "w") as f:
    f.write(transcription)
print(f"Transcription saved to: {transcription_file}")

# Also perform ASR on the original audio for comparison
print("Transcribing original audio...")
original_transcription = asr_model.transcribe_file(input_file)
print(f"Original transcription: {original_transcription}")

# Save original transcription to file
with open(os.path.join(output_dir, "output_original_transcription.txt"), "w") as f:
    f.write(original_transcription)

print("Processing complete!")