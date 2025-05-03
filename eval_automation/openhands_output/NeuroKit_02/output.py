#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EDA (Electrodermal Activity) Analysis Script
This script processes EDA data using NeuroKit2 and extracts relevant features.
"""

import os
import pandas as pd
import numpy as np
import neurokit2 as nk
import matplotlib.pyplot as plt
from pathlib import Path

# Define file paths
input_file = "/data/data/agent_test_codebase/GitTaskBench/queries/NeuroKit_02/input/eda_analysis_01_input.csv"
output_dir = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/NeuroKit_02"
output_file = os.path.join(output_dir, "output.csv")
output_plot = os.path.join(output_dir, "output_plot.png")
output_features = os.path.join(output_dir, "output_features.csv")

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Load the data
print("Loading data...")
data = pd.read_csv(input_file)

# Assuming a sampling rate of 100 Hz (common for physiological data)
# If the actual sampling rate is known, it should be used instead
sampling_rate = 100

# Extract EDA signal
eda_signal = data["EDA"].values

# Process EDA signal
print("Processing EDA signal...")
eda_processed, info = nk.eda_process(eda_signal, sampling_rate=sampling_rate)

# Reset index to make sure we have integer indices
eda_processed = eda_processed.reset_index(drop=True)

# Save processed data
eda_processed.to_csv(output_file, index=False)
print(f"Processed data saved to {output_file}")

# Plot the processed EDA signal
print("Generating plots...")
fig = plt.figure(figsize=(12, 8))
nk.eda_plot(eda_processed, info)
plt.tight_layout()
plt.savefig(output_plot, dpi=300)
plt.close()
print(f"Plot saved to {output_plot}")

# Extract EDA features
print("Extracting EDA features...")

# Get SCR (Skin Conductance Response) peaks information
scr_peaks = info["SCR_Peaks"]
scr_onsets = info["SCR_Onsets"]
scr_recoveries = info["SCR_Recovery"]

# Print types for debugging
print(f"Type of SCR_Peaks: {type(scr_peaks)}")
print(f"First few peaks: {scr_peaks[:5] if len(scr_peaks) > 0 else 'No peaks'}")
print(f"First few onsets: {scr_onsets[:5] if len(scr_onsets) > 0 else 'No onsets'}")
print(f"First few recoveries: {scr_recoveries[:5] if len(scr_recoveries) > 0 else 'No recoveries'}")

# Convert to integers if needed, handling NaN values
scr_peaks = [int(peak) for peak in scr_peaks if not np.isnan(peak)]
scr_onsets = [int(onset) for onset in scr_onsets if not np.isnan(onset)]
scr_recoveries = [int(recovery) for recovery in scr_recoveries if not np.isnan(recovery)]

# Calculate basic features
features = {}

# Number of SCR peaks
features["SCR_Peaks_Count"] = len(scr_peaks)

# If there are peaks, calculate more features
if len(scr_peaks) > 0:
    # SCR amplitudes
    amplitudes = []
    rise_times = []
    recovery_times = []
    half_recovery_times = []
    
    for i, peak in enumerate(scr_peaks):
        if i < len(scr_onsets):
            onset = scr_onsets[i]
            # Amplitude: difference between peak and onset values
            amplitude = eda_processed["EDA_Phasic"].iloc[peak] - eda_processed["EDA_Phasic"].iloc[onset]
            amplitudes.append(amplitude)
            
            # Rise time: time from onset to peak
            rise_time = (peak - onset) / sampling_rate
            rise_times.append(rise_time)
            
            # Recovery time (if recovery point exists)
            if i < len(scr_recoveries) and scr_recoveries[i] > 0:
                recovery = scr_recoveries[i]
                recovery_time = (recovery - peak) / sampling_rate
                recovery_times.append(recovery_time)
                
                # Half recovery time (time to reach 50% of amplitude)
                half_amp = amplitude / 2
                peak_value = eda_processed["EDA_Phasic"].iloc[peak]
                target_value = peak_value - half_amp
                
                # Get indices between peak and recovery
                indices_between = np.arange(peak, recovery)
                
                # Find where the signal drops below half amplitude
                if len(indices_between) > 0:
                    for idx in indices_between:
                        if idx < len(eda_processed) and eda_processed["EDA_Phasic"].iloc[idx] <= target_value:
                            half_recovery_time = (idx - peak) / sampling_rate
                            half_recovery_times.append(half_recovery_time)
                            break
    
    # Calculate statistics for the features
    features["SCR_Amplitude_Mean"] = np.mean(amplitudes) if amplitudes else np.nan
    features["SCR_Amplitude_Std"] = np.std(amplitudes) if amplitudes else np.nan
    features["SCR_Amplitude_Max"] = np.max(amplitudes) if amplitudes else np.nan
    features["SCR_Amplitude_Min"] = np.min(amplitudes) if amplitudes else np.nan
    
    features["SCR_RiseTime_Mean"] = np.mean(rise_times) if rise_times else np.nan
    features["SCR_RiseTime_Std"] = np.std(rise_times) if rise_times else np.nan
    
    features["SCR_RecoveryTime_Mean"] = np.mean(recovery_times) if recovery_times else np.nan
    features["SCR_RecoveryTime_Std"] = np.std(recovery_times) if recovery_times else np.nan
    
    features["SCR_HalfRecoveryTime_Mean"] = np.mean(half_recovery_times) if half_recovery_times else np.nan
    features["SCR_HalfRecoveryTime_Std"] = np.std(half_recovery_times) if half_recovery_times else np.nan

# Calculate tonic features (from the tonic component)
features["EDA_Tonic_Mean"] = eda_processed["EDA_Tonic"].mean()
features["EDA_Tonic_Std"] = eda_processed["EDA_Tonic"].std()
features["EDA_Tonic_Max"] = eda_processed["EDA_Tonic"].max()
features["EDA_Tonic_Min"] = eda_processed["EDA_Tonic"].min()

# Calculate phasic features (from the phasic component)
features["EDA_Phasic_Mean"] = eda_processed["EDA_Phasic"].mean()
features["EDA_Phasic_Std"] = eda_processed["EDA_Phasic"].std()
features["EDA_Phasic_Max"] = eda_processed["EDA_Phasic"].max()
features["EDA_Phasic_Min"] = eda_processed["EDA_Phasic"].min()

# Calculate SCR rate (SCRs per minute)
duration_minutes = len(eda_signal) / sampling_rate / 60
features["SCR_Rate"] = features["SCR_Peaks_Count"] / duration_minutes

# Save features to CSV
features_df = pd.DataFrame(features, index=[0])
features_df.to_csv(output_features, index=False)
print(f"EDA features saved to {output_features}")

# Also use NeuroKit's built-in feature extraction
print("Extracting additional features using NeuroKit...")
eda_features = nk.eda_intervalrelated(eda_processed)
eda_features.to_csv(os.path.join(output_dir, "output_nk_features.csv"), index=False)

print("EDA analysis completed successfully!")