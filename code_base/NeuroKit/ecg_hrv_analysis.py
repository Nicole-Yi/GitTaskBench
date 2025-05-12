import csv
import numpy as np
import math

# Minimal ECG processing without SciPy
def ecg_process(ecg, sampling_rate=1000):
    # Simple moving average filter as alternative to bandpass
    window_size = int(sampling_rate/25)  # ~40ms window
    filtered = np.convolve(ecg, np.ones(window_size)/window_size, mode='same')
    
    # Basic peak detection using zero-crossing of derivative
    diff = np.diff(filtered)
    peaks = np.where((diff[:-1] > 0) & (diff[1:] < 0))[0] + 1
    
    return {"ECG_Filtered": filtered, "ECG_R_Peaks": peaks}, {"sampling_rate": sampling_rate}

# Minimal HRV calculation
def hrv_features(peaks, sampling_rate):
    rr_intervals = np.diff(peaks) / sampling_rate * 1000  # in ms
    return {
        "HRV_MeanNN": np.mean(rr_intervals),
        "HRV_SDNN": np.std(rr_intervals),
        "HRV_RMSSD": np.sqrt(np.mean(np.square(np.diff(rr_intervals))))
    }

# Load ECG data without pandas
ecg = []
with open("/data/data/agent_test_codebase/GitTaskBench/queries/NeuroKit_01/input/ecg_hrv_analysis_01_input.csv") as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        ecg.append(float(row[0]))  # First column is ECG
ecg = np.array(ecg)

# Process ECG and detect R-peaks
ecg_signals, info = ecg_process(ecg, sampling_rate=1000)  # Assuming 1kHz sampling rate

# Calculate basic HRV metrics
hrv_results = hrv_features(ecg_signals["ECG_R_Peaks"], sampling_rate=1000)

# Save results
output_dir = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/NeuroKit_01"
with open(f"{output_dir}/output.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(hrv_results.keys())
    writer.writerow(hrv_results.values())

print("Basic HRV analysis completed. Results saved to:", output_dir)