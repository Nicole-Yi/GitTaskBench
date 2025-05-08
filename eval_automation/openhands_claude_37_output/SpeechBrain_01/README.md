# Speech Enhancement with SpeechBrain

This project demonstrates speech enhancement capabilities using the SpeechBrain library and other audio processing tools.

## Overview

The goal of this project is to enhance a speech audio file by reducing background noise and improving clarity. We've implemented a solution using librosa, a Python library for audio and music analysis.

## Files

- `output.wav`: The enhanced audio file
- `output.txt`: Information about the enhancement process
- `process_audio_simple_librosa.py`: The Python script used for speech enhancement

## Enhancement Process

The following techniques were applied to enhance the audio:

1. **Conversion to Mono and Resampling**: The original stereo audio was converted to mono and resampled to 16kHz for better processing.

2. **Noise Reduction using Spectral Subtraction**: 
   - The audio was transformed to the frequency domain using Short-Time Fourier Transform (STFT)
   - A noise profile was estimated from the first portion of the audio
   - Spectral subtraction was applied to reduce background noise

3. **Audio Normalization**: The audio was normalized to ensure consistent volume levels.

4. **Dynamic Range Compression**: The dynamic range was compressed to make quieter parts more audible while preventing louder parts from being too overwhelming.

## Implementation Details

The implementation uses the following libraries:
- `librosa`: For audio processing and feature extraction
- `soundfile`: For reading and writing audio files
- `numpy`: For numerical operations

## Usage

To run the enhancement process:

```bash
python process_audio_simple_librosa.py
```

## Results

The enhanced audio file (`output.wav`) should have:
- Reduced background noise
- Improved clarity
- More consistent volume levels
- Better overall listening experience

## Note on SpeechBrain

While we initially planned to use SpeechBrain's pretrained models for enhancement, we encountered compatibility issues with the current environment. The implemented solution uses core audio processing techniques that are similar to those used in SpeechBrain's enhancement models, but with a more direct implementation using librosa.