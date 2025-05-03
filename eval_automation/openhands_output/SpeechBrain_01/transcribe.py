
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
