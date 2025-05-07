
import neurokit2 as nk
import pandas as pd

# Read ECG data from CSV
ecg_data = pd.read_csv('/data/data/agent_test_codebase/GitTaskBench/queries/NeuroKit_01/input/ecg_hrv_analysis_01_input.csv')

# Assume the ECG data is in a column named "ECG"
ecg_signal = ecg_data['ECG'].values

# Process the ECG signal (sampling rate needs confirmation, assuming 1000 Hz)
signals, info = nk.ecg_process(ecg_signal, sampling_rate=1000)

# Calculate HRV indices
hrv_indices = nk.hrv(info, sampling_rate=1000)

# Write the HRV results to CSV
hrv_indices.to_csv('/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/NeuroKit_01/output.csv')