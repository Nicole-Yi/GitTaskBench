# Speech Enhancement Solution

This directory contains the results of speech enhancement processing on the input file.

## Files

- `output.wav`: Enhanced audio using Wiener filtering
- `output_spectral.wav`: Enhanced audio using Spectral Subtraction
- `output_combined.wav`: Enhanced audio using a combination of both methods (Spectral Subtraction followed by Wiener filtering)

## Methods Used

### Wiener Filtering

Wiener filtering is a statistical approach to noise reduction that estimates the clean speech signal by minimizing the mean square error between the estimated and the actual clean speech signal. It works by:

1. Computing the STFT (Short-Time Fourier Transform) of the noisy signal
2. Estimating the noise power spectrum from the first few frames (assuming they contain mostly noise)
3. Computing the a priori SNR (Signal-to-Noise Ratio)
4. Applying the Wiener filter gain to the noisy spectrum
5. Reconstructing the signal using inverse STFT

### Spectral Subtraction

Spectral subtraction is a simple but effective method for noise reduction that works by:

1. Computing the STFT of the noisy signal
2. Estimating the noise magnitude spectrum from the first few frames
3. Subtracting the noise estimate from the noisy magnitude spectrum
4. Applying a noise floor to prevent musical noise
5. Reconstructing the signal using the original phase and enhanced magnitude

### Combined Method

The combined method applies both techniques sequentially:

1. First, spectral subtraction is applied to reduce the background noise
2. Then, Wiener filtering is applied to further enhance the speech signal

## Implementation

The implementation is based on the SpeechEnhance repository, but uses custom implementations of classical speech enhancement algorithms since the original model requires training data that was not available.

The code can be found in the following files:
- `simple_denoise.py`: Implements Wiener filtering and Spectral Subtraction
- `combined_denoise.py`: Implements the combined approach