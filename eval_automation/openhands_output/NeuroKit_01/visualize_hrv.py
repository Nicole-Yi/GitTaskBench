#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Visualization of HRV Metrics

This script creates visualizations of the HRV metrics calculated by the main analysis script.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the style
sns.set(style="whitegrid")

# Define file paths
output_dir = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/NeuroKit_01"
hrv_file = os.path.join(output_dir, "output_02_hrv_indices.csv")

# Load HRV data
hrv_data = pd.read_csv(hrv_file)

# Select key HRV metrics for visualization
key_metrics = [
    "HRV_MeanNN", "HRV_SDNN", "HRV_RMSSD", "HRV_pNN50", 
    "HRV_LF", "HRV_HF", "HRV_LFHF", 
    "HRV_SD1", "HRV_SD2", "HRV_SD1SD2",
    "HRV_SampEn", "HRV_DFA_alpha1"
]

# Create a subset of the data with only the key metrics
key_data = pd.DataFrame()
for metric in key_metrics:
    if metric in hrv_data.columns:
        key_data[metric] = hrv_data[metric]

# Transpose the data for better visualization
key_data_t = key_data.T.reset_index()
key_data_t.columns = ["Metric", "Value"]

# Create a bar plot of the key metrics
plt.figure(figsize=(12, 8))
ax = sns.barplot(x="Metric", y="Value", data=key_data_t)
plt.title("Key HRV Metrics", fontsize=16)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

# Save the plot
hrv_plot_file = os.path.join(output_dir, "output_05_key_hrv_metrics.png")
plt.savefig(hrv_plot_file)
print(f"Key HRV metrics plot saved to: {hrv_plot_file}")

# Create a Poincaré plot if SD1 and SD2 are available
if "HRV_SD1" in hrv_data.columns and "HRV_SD2" in hrv_data.columns:
    sd1 = hrv_data["HRV_SD1"].values[0]
    sd2 = hrv_data["HRV_SD2"].values[0]
    
    # Load RR intervals
    processed_ecg_file = os.path.join(output_dir, "output_01_processed_ecg.csv")
    ecg_data = pd.read_csv(processed_ecg_file)
    
    # Create a simulated Poincaré plot based on SD1 and SD2
    plt.figure(figsize=(8, 8))
    
    # Create an ellipse representing the Poincaré plot
    from matplotlib.patches import Ellipse
    
    # Center of the ellipse
    center = (1000, 1000)  # Typical RR interval in ms
    
    # Create the ellipse
    ellipse = Ellipse(xy=center, width=2*sd2, height=2*sd1, 
                      edgecolor='blue', fc='none', lw=2)
    
    # Plot
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.add_patch(ellipse)
    
    # Add lines representing SD1 and SD2
    ax.plot([center[0] - sd2, center[0] + sd2], [center[1], center[1]], 'r-', lw=2)
    ax.plot([center[0], center[0]], [center[1] - sd1, center[1] + sd1], 'g-', lw=2)
    
    # Add text annotations
    ax.text(center[0] + sd2 + 10, center[1], f"SD2 = {sd2:.2f} ms", 
            color='red', fontsize=12, va='center')
    ax.text(center[0], center[1] + sd1 + 10, f"SD1 = {sd1:.2f} ms", 
            color='green', fontsize=12, ha='center')
    
    # Set axis limits
    ax.set_xlim(center[0] - sd2*1.5, center[0] + sd2*1.5)
    ax.set_ylim(center[1] - sd1*1.5, center[1] + sd1*1.5)
    
    # Labels and title
    ax.set_xlabel("RR$_n$ (ms)", fontsize=14)
    ax.set_ylabel("RR$_{n+1}$ (ms)", fontsize=14)
    ax.set_title("Poincaré Plot", fontsize=16)
    
    # Add SD1/SD2 ratio
    ax.text(center[0] - sd2, center[1] - sd1, 
            f"SD1/SD2 = {sd1/sd2:.3f}", fontsize=12)
    
    plt.tight_layout()
    
    # Save the plot
    poincare_plot_file = os.path.join(output_dir, "output_06_poincare_plot.png")
    plt.savefig(poincare_plot_file)
    print(f"Poincaré plot saved to: {poincare_plot_file}")

print("Visualization complete!")