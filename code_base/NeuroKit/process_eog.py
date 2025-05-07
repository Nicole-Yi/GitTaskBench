
import pandas as pd
import neurokit2 as nk

# Input and output paths
input_csv = "/data/data/agent_test_codebase/GitTaskBench/queries/NeuroKit_03/input/NeuroKit_03_input.csv"
output_dir = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/NeuroKit_03/output.csv"

# Read input CSV
input_data = pd.read_csv(input_csv)

# Assume PhotoSensor column is EOG
photo_sensor_data = input_data["PhotoSensor"]

# Process EOG data
results, info = nk.eog_process(photo_sensor_data, sampling_rate=1000)

# Extract metrics
mean_resp_rate_bpm = results["EOG_Rate"].mean()
peak_times_seconds = info["Blink_Onsets"] / 1000  # Convert to seconds
number_of_peaks = len(info["Blink_Onsets"])

# Prepare and write output CSV
output_data = pd.DataFrame({
    "Mean_Respiratory_Rate_BPM": [mean_resp_rate_bpm],
    "Peak_Times_Seconds": [list(peak_times_seconds)],
    "Number_of_Peaks": [number_of_peaks]
})

output_data.to_csv(output_dir, index=False)

print("EOG Processing completed successfully, output written to:", output_dir)