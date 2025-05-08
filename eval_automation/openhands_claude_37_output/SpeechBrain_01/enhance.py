
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
