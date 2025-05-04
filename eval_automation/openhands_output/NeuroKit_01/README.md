# ECG Analysis and Heart Rate Variability (HRV) Calculation

This directory contains the results of ECG signal processing and HRV analysis performed using the NeuroKit2 library.

## Input Data

The analysis was performed on ECG data from the file:
`/data/data/agent_test_codebase/GitTaskBench/queries/NeuroKit_01/input/ecg_hrv_analysis_01_input.csv`

## Output Files

1. **output.csv**: A comprehensive report containing:
   - ECG recording duration
   - Number of detected R-peaks
   - Heart rate statistics (mean, min, max)
   - All calculated HRV metrics

2. **output_01_processed_ecg.csv**: Contains the processed ECG data including:
   - Raw ECG signal
   - Cleaned ECG signal
   - R-peak detection results
   - Heart rate time series

3. **output_02_hrv_indices.csv**: Detailed HRV metrics including:
   - Time-domain metrics (SDNN, RMSSD, pNN50, etc.)
   - Frequency-domain metrics (LF, HF, LF/HF ratio, etc.)
   - Non-linear metrics (SD1, SD2, entropy measures, etc.)

4. **output_03_ecg_plot.png**: Visualization of:
   - Raw ECG signal
   - Cleaned ECG signal with marked R-peaks

5. **output_04_heart_rate_plot.png**: Visualization of the heart rate time series

6. **output_05_key_hrv_metrics.png**: Bar plot of key HRV metrics for easy comparison

7. **output_06_poincare_plot.png**: Poincaré plot visualization showing:
   - SD1 (standard deviation perpendicular to the line of identity)
   - SD2 (standard deviation along the line of identity)
   - SD1/SD2 ratio (indicator of the ratio between short and long-term HRV)

## Analysis Summary

- **Recording Duration**: 68.61 seconds
- **Number of R-peaks Detected**: 65
- **Mean Heart Rate**: 56.82 BPM
- **Key HRV Metrics**:
  - SDNN: 73.67 ms (Standard deviation of NN intervals)
  - RMSSD: 61.14 ms (Root mean square of successive differences)
  - pNN50: 37.5% (Percentage of successive NN intervals that differ by more than 50 ms)
  - LF/HF Ratio: 1.55 (Ratio of low frequency to high frequency power)

## Methods

The analysis was performed using the following steps:

1. **ECG Signal Cleaning**: The raw ECG signal was cleaned using NeuroKit2's `ecg_clean()` function.
2. **R-peak Detection**: R-peaks were detected using NeuroKit2's `ecg_peaks()` function.
3. **Heart Rate Calculation**: Heart rate was calculated from the detected R-peaks.
4. **HRV Analysis**: HRV metrics were calculated using NeuroKit2's `hrv()` function.

## References

- Makowski, D., Pham, T., Lau, Z. J., Brammer, J. C., Lespinasse, F., Pham, H., Schölzel, C., & Chen, S. A. (2021). NeuroKit2: A Python toolbox for neurophysiological signal processing. Behavior Research Methods, 53(4), 1689–1696. https://doi.org/10.3758/s13428-020-01516-y