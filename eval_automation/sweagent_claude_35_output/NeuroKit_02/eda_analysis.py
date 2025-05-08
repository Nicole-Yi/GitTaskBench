
import pandas as pd
import sys
import os
import numpy as np

def sanitize_signal(signal):
    """Basic signal cleaning"""
    # Remove outliers (values beyond 3 standard deviations)
    mean = np.mean(signal)
    std = np.std(signal)
    clean_signal = np.clip(signal, mean - 3*std, mean + 3*std)
    return clean_signal

def process_eda(signal):
    """Basic EDA signal processing"""
    # Remove linear trend
    x = np.arange(len(signal))
    z = np.polyfit(x, signal, 1)
    p = np.poly1d(z)
    trend = p(x)
    detrended = signal - trend
    
    # Normalize
    normalized = (detrended - np.mean(detrended)) / np.std(detrended)
    return normalized

def extract_eda_features(signal):
    """Extract basic EDA features"""
    features = {
        'EDA_Mean': np.mean(signal),
        'EDA_Std': np.std(signal),
        'EDA_Min': np.min(signal),
        'EDA_Max': np.max(signal),
        'EDA_Range': np.ptp(signal),
        'EDA_Median': np.median(signal),
        'EDA_Q1': np.percentile(signal, 25),
        'EDA_Q3': np.percentile(signal, 75),
        'EDA_IQR': np.percentile(signal, 75) - np.percentile(signal, 25)
    }
    return pd.DataFrame([features])

# Read the input data
input_file = '/data/data/agent_test_codebase/GitTaskBench/queries/NeuroKit_02/input/eda_analysis_01_input.csv'
output_dir = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/NeuroKit_02'

try:
    # Read the CSV file
    data = pd.read_csv(input_file)
    print("Data shape:", data.shape)
    print("Data columns:", data.columns)
    print("First few rows:", data.head())
    
    # Get the EDA signal
    eda_signal = data['EDA'].values
    print("EDA signal shape:", eda_signal.shape)
    print("EDA signal first few values:", eda_signal[:5])
    
    # Clean and process the signal
    eda_clean = sanitize_signal(eda_signal)
    eda_processed = process_eda(eda_clean)
    
    # Create processed signals DataFrame
    signals = pd.DataFrame({
        'EDA_Raw': eda_signal,
        'EDA_Clean': eda_clean,
        'EDA_Processed': eda_processed
    })
    
    # Extract features
    eda_features = extract_eda_features(eda_clean)
except Exception as e:
    print(f"Error processing EDA data: {str(e)}")
    sys.exit(1)

# Save the processed signals
signals.to_csv(os.path.join(output_dir, 'output_01_processed_signals.csv'), index=False)

# Save the features
eda_features.to_csv(os.path.join(output_dir, 'output_02_eda_features.csv'), index=True)

print("EDA analysis completed successfully. Results saved in the output directory.")