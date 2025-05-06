
import pandas as pd
import numpy as np

def find_r_peaks(ecg_signal, sampling_rate):
    # Calculate the gradient of the signal
    gradient = np.gradient(ecg_signal)
    
    # Find potential R-peaks (points where gradient changes from positive to negative)
    potential_peaks = []
    for i in range(1, len(gradient)-1):
        if gradient[i-1] > 0 and gradient[i+1] < 0:
            potential_peaks.append(i)
    
    # Filter peaks based on minimum distance and amplitude
    min_distance = int(sampling_rate * 0.2)  # Minimum 200ms between peaks
    filtered_peaks = []
    last_peak = -min_distance
    
    for peak in potential_peaks:
        if peak - last_peak >= min_distance and ecg_signal[peak] > np.mean(ecg_signal):
            filtered_peaks.append(peak)
            last_peak = peak
    
    return np.array(filtered_peaks)

def calculate_hrv_metrics(rr_intervals_ms):
    # Time domain metrics
    mean_rr = np.mean(rr_intervals_ms)
    sdnn = np.std(rr_intervals_ms)
    rmssd = np.sqrt(np.mean(np.diff(rr_intervals_ms) ** 2))
    
    # Calculate NN50 and pNN50
    nn50 = sum(abs(np.diff(rr_intervals_ms)) > 50)
    pnn50 = (nn50 / len(rr_intervals_ms)) * 100
    
    metrics = {
        'MeanRR': mean_rr,
        'SDNN': sdnn,
        'RMSSD': rmssd,
        'pNN50': pnn50
    }
    return pd.DataFrame([metrics])

# Read the input ECG data
input_file = "/data/data/agent_test_codebase/GitTaskBench/queries/NeuroKit_01/input/ecg_hrv_analysis_01_input.csv"
output_file = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/NeuroKit_01/output.csv"

# Read the ECG data
data = pd.read_csv(input_file)
ecg_signal = data['ECG'].values
sampling_rate = 1000  # Assuming 1000 Hz sampling rate

# Find R-peaks
r_peaks = find_r_peaks(ecg_signal, sampling_rate)

# Calculate RR intervals in milliseconds
rr_intervals = np.diff(r_peaks) * (1000 / sampling_rate)

# Calculate HRV metrics
hrv_metrics = calculate_hrv_metrics(rr_intervals)

# Save results
hrv_metrics.to_csv(output_file, index=False)
print(f"HRV analysis completed. Results saved to {output_file}")