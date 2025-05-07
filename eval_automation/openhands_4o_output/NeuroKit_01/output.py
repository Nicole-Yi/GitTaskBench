import pandas as pd
import neurokit2 as nk

# Paths to input and output files
data_path = '/data/data/agent_test_codebase/GitTaskBench/queries/NeuroKit_01/input/ecg_hrv_analysis_01_input.csv'
output_path = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/NeuroKit_01/output.csv'

# Load ECG data from the CSV file
data = pd.read_csv(data_path)

# Extract the ECG column
ecg_signal = data['ECG']

# Process ECG signal
ecg_signals, ecg_info = nk.ecg_process(ecg_signal, sampling_rate=1000)

# Compute HRV indices
hrv_indices = nk.hrv(ecg_info['ECG_R_Peaks'], sampling_rate=1000)

# Save HRV results to CSV
hrv_indices.to_csv(output_path, index=False)
