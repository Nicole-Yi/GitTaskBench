#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EDA Analysis Results Viewer
This script loads and displays the results of the EDA analysis.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set paths
output_dir = os.path.dirname(os.path.abspath(__file__))
processed_data_file = os.path.join(output_dir, "output.csv")
features_file = os.path.join(output_dir, "output_features.csv")
nk_features_file = os.path.join(output_dir, "output_nk_features.csv")

# Load data
processed_data = pd.read_csv(processed_data_file)
features = pd.read_csv(features_file)
nk_features = pd.read_csv(nk_features_file)

# Print summary
print("=" * 50)
print("EDA ANALYSIS SUMMARY")
print("=" * 50)

print("\nProcessed Data Shape:", processed_data.shape)
print("\nProcessed Data Columns:")
for col in processed_data.columns:
    print(f"  - {col}")

print("\nExtracted Features:")
for col in features.columns:
    value = features[col].values[0]
    print(f"  - {col}: {value:.4f}")

print("\nNeuroKit Features:")
for col in nk_features.columns:
    if pd.notna(nk_features[col].values[0]):
        value = nk_features[col].values[0]
        print(f"  - {col}: {value:.4f}")

# Create a summary plot
plt.figure(figsize=(15, 10))

# Plot 1: Raw EDA signal with tonic component
plt.subplot(3, 1, 1)
plt.plot(processed_data["EDA_Raw"], label="Raw EDA", alpha=0.7)
plt.plot(processed_data["EDA_Tonic"], label="Tonic Component", linewidth=2)
plt.title("Raw EDA Signal and Tonic Component")
plt.legend()
plt.grid(True, alpha=0.3)

# Plot 2: Phasic component
plt.subplot(3, 1, 2)
plt.plot(processed_data["EDA_Phasic"], label="Phasic Component")
plt.title("Phasic Component (Fast-changing)")
plt.legend()
plt.grid(True, alpha=0.3)

# Plot 3: SCR (clean phasic with peaks)
plt.subplot(3, 1, 3)
plt.plot(processed_data["EDA_Phasic"], label="Phasic Component", alpha=0.7)
plt.plot(processed_data["SCR_Peaks"], 'ro', label="SCR Peaks")
plt.title("SCR Peaks Detection")
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "summary_plot.png"), dpi=300)
print(f"\nSummary plot saved to {os.path.join(output_dir, 'summary_plot.png')}")

print("\nEDA Analysis Summary Complete!")