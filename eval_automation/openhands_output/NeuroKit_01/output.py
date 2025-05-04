#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ECG Analysis and Heart Rate Variability (HRV) Calculation using NeuroKit2

This script processes ECG data from a CSV file, performs ECG signal processing,
and calculates various HRV metrics. The results are saved to CSV files.
"""

import os
import numpy as np
import pandas as pd
import neurokit2 as nk
import matplotlib.pyplot as plt
from scipy import signal

# Define file paths
input_file = "/data/data/agent_test_codebase/GitTaskBench/queries/NeuroKit_01/input/ecg_hrv_analysis_01_input.csv"
output_dir = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/NeuroKit_01"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Load the data
print("Loading data from:", input_file)
data = pd.read_csv(input_file)

# Extract ECG signal
ecg_signal = data["ECG"].values

# Determine sampling rate based on data characteristics
# For this example, we'll use 100 Hz which is a common sampling rate for ECG
sampling_rate = 100  # 100 Hz is a common sampling rate for ECG data

print(f"Data length: {len(ecg_signal)} samples")
print(f"Using sampling rate: {sampling_rate} Hz")
print(f"Estimated recording duration: {len(ecg_signal)/sampling_rate:.2f} seconds")

# First, let's clean the ECG signal
print("Cleaning ECG signal...")
ecg_cleaned = nk.ecg_clean(ecg_signal, sampling_rate=sampling_rate)

# Find R-peaks in the cleaned signal
print("Finding R-peaks...")
rpeaks, info_peaks = nk.ecg_peaks(ecg_cleaned, sampling_rate=sampling_rate)

# Check if R-peaks were found
if len(info_peaks["ECG_R_Peaks"]) < 2:
    print("Warning: Too few R-peaks detected. Trying alternative method...")
    # Try alternative method with different parameters
    ecg_cleaned = nk.ecg_clean(ecg_signal, sampling_rate=sampling_rate, method="neurokit")
    rpeaks, info_peaks = nk.ecg_peaks(ecg_cleaned, sampling_rate=sampling_rate, method="pantompkins")

print(f"Number of R-peaks detected: {len(info_peaks['ECG_R_Peaks'])}")

# Create a DataFrame with the processed ECG data
signals = pd.DataFrame({
    "ECG_Raw": ecg_signal,
    "ECG_Clean": ecg_cleaned,
    "ECG_R_Peaks": rpeaks["ECG_R_Peaks"]
})

# Calculate heart rate
print("Calculating heart rate...")
heart_rate = nk.signal_rate(info_peaks["ECG_R_Peaks"], sampling_rate=sampling_rate, desired_length=len(ecg_cleaned))
signals["ECG_Rate"] = heart_rate

# Save processed ECG data
processed_ecg_file = os.path.join(output_dir, "output_01_processed_ecg.csv")
signals.to_csv(processed_ecg_file, index=False)
print(f"Processed ECG data saved to: {processed_ecg_file}")

# Calculate HRV indices if enough R-peaks were detected
if len(info_peaks["ECG_R_Peaks"]) >= 2:
    print("Calculating HRV metrics...")
    try:
        hrv_indices = nk.hrv(info_peaks["ECG_R_Peaks"], sampling_rate=sampling_rate)
        
        # Save HRV indices
        hrv_file = os.path.join(output_dir, "output_02_hrv_indices.csv")
        hrv_indices.to_csv(hrv_file, index=False)
        print(f"HRV indices saved to: {hrv_file}")
    except Exception as e:
        print(f"Error calculating HRV indices: {e}")
        # Create an empty DataFrame for HRV indices
        hrv_indices = pd.DataFrame()
else:
    print("Not enough R-peaks detected to calculate HRV metrics.")
    hrv_indices = pd.DataFrame()

# Generate visualizations
print("Generating visualizations...")

# Plot processed ECG signal
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(signals["ECG_Raw"])
plt.title("Raw ECG Signal")
plt.xlabel("Samples")
plt.ylabel("Amplitude")

plt.subplot(2, 1, 2)
plt.plot(signals["ECG_Clean"])
plt.title("Cleaned ECG Signal")
plt.xlabel("Samples")
plt.ylabel("Amplitude")

# Mark R-peaks
for peak in info_peaks["ECG_R_Peaks"]:
    if peak < len(signals):
        plt.axvline(x=peak, color='red', linestyle='--', alpha=0.5)

plt.tight_layout()
ecg_plot_file = os.path.join(output_dir, "output_03_ecg_plot.png")
plt.savefig(ecg_plot_file)
print(f"ECG plot saved to: {ecg_plot_file}")

# Plot heart rate if available
if "ECG_Rate" in signals.columns and not signals["ECG_Rate"].isna().all():
    plt.figure(figsize=(12, 4))
    plt.plot(signals["ECG_Rate"])
    plt.title("Heart Rate")
    plt.xlabel("Samples")
    plt.ylabel("Heart Rate (BPM)")
    hr_plot_file = os.path.join(output_dir, "output_04_heart_rate_plot.png")
    plt.savefig(hr_plot_file)
    print(f"Heart rate plot saved to: {hr_plot_file}")

# Generate a comprehensive report
report = {
    "ECG_Duration_Seconds": len(ecg_signal) / sampling_rate,
    "Number_of_R_Peaks": len(info_peaks["ECG_R_Peaks"]),
}

# Add heart rate statistics if available
if "ECG_Rate" in signals.columns and not signals["ECG_Rate"].isna().all():
    valid_rates = signals["ECG_Rate"].dropna()
    if len(valid_rates) > 0:
        report.update({
            "Mean_Heart_Rate": valid_rates.mean(),
            "Min_Heart_Rate": valid_rates.min(),
            "Max_Heart_Rate": valid_rates.max(),
        })

# Add HRV metrics to the report if available
if not hrv_indices.empty:
    for column in hrv_indices.columns:
        report[column] = hrv_indices[column].values[0]

# Save report as CSV
report_df = pd.DataFrame([report])
report_file = os.path.join(output_dir, "output.csv")
report_df.to_csv(report_file, index=False)
print(f"Comprehensive report saved to: {report_file}")

print("Analysis complete!")