# EDA (Electrodermal Activity) Analysis

This directory contains the results of EDA (skin conductance) data analysis performed using the NeuroKit2 library.

## Files

- `output.py`: Python script used for processing the EDA data and extracting features
- `output.csv`: Processed EDA signal data with tonic and phasic components
- `output_plot.png`: Visualization of the EDA signal processing, showing raw signal, tonic component, phasic component, and detected SCR peaks
- `output_features.csv`: Extracted EDA features from custom analysis
- `output_nk_features.csv`: Features extracted using NeuroKit2's built-in feature extraction

## EDA Features Explanation

### Custom Features (`output_features.csv`)

- **SCR_Peaks_Count**: Number of Skin Conductance Response (SCR) peaks detected
- **SCR_Amplitude_Mean/Std/Max/Min**: Statistics of SCR amplitudes (difference between peak and onset values)
- **SCR_RiseTime_Mean/Std**: Statistics of rise times (time from onset to peak)
- **SCR_RecoveryTime_Mean/Std**: Statistics of recovery times (time from peak to recovery point)
- **SCR_HalfRecoveryTime_Mean/Std**: Statistics of half recovery times (time to reach 50% of amplitude)
- **EDA_Tonic_Mean/Std/Max/Min**: Statistics of the tonic (slow-changing) component of the EDA signal
- **EDA_Phasic_Mean/Std/Max/Min**: Statistics of the phasic (fast-changing) component of the EDA signal
- **SCR_Rate**: Number of SCR peaks per minute

### NeuroKit Features (`output_nk_features.csv`)

- **SCR_Peaks_N**: Number of SCR peaks detected
- **SCR_Peaks_Amplitude_Mean**: Mean amplitude of SCR peaks
- **EDA_Tonic_SD**: Standard deviation of the tonic component
- **EDA_Sympathetic**: Sympathetic activity index (if available)
- **EDA_SympatheticN**: Normalized sympathetic activity index (if available)
- **EDA_Autocorrelation**: Autocorrelation of the EDA signal (if available)

## Methodology

The analysis follows these steps:

1. **Signal Processing**:
   - The raw EDA signal is cleaned and filtered
   - The signal is decomposed into tonic (slow-changing) and phasic (fast-changing) components
   - SCR peaks, onsets, and recovery points are detected in the phasic component

2. **Feature Extraction**:
   - Time-domain features are calculated from the processed signal
   - SCR characteristics (amplitude, rise time, recovery time) are computed
   - Statistical measures (mean, std, min, max) are calculated for relevant components

3. **Visualization**:
   - The processed signal and its components are plotted for visual inspection
   - SCR peaks are marked on the plot

## Usage

The analysis was performed with a sampling rate of 100 Hz. If the actual sampling rate is different, the script should be modified accordingly.