import neurokit2 as nk
import pandas as pd

# Load input data
data = pd.read_csv("/data/data/agent_test_codebase/GitTaskBench/queries/NeuroKit_03/input/NeuroKit_03_input.csv")

# Assuming first column is EOG data
eog_signal = data.iloc[:,0]

# Process EOG data
signals, info = nk.eog_process(eog_signal, sampling_rate=100)  # Assuming 100Hz sampling rate

# Extract requested metrics
results = {
    "Mean_Respiratory_Rate_BPM": signals["EOG_Rate"].mean(),
    "Peak_Times_Seconds": list(signals[signals["EOG_Blinks"] == 1].index / 100),  # Convert to seconds
    "Number_of_Peaks": signals["EOG_Blinks"].sum()
}

# Save results
output_df = pd.DataFrame({
    "Metric": ["Mean_Respiratory_Rate_BPM", "Number_of_Peaks"],
    "Value": [results["Mean_Respiratory_Rate_BPM"], results["Number_of_Peaks"]]
})

peaks_df = pd.DataFrame({
    "Peak_Times_Seconds": results["Peak_Times_Seconds"]
})

output_df.to_csv("/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/NeuroKit_03/output_metrics.csv", index=False)
peaks_df.to_csv("/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/NeuroKit_03/output_peaks.csv", index=False)