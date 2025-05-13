import pandas as pd
import neurokit2 as nk
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv("/data/data/agent_test_codebase/GitTaskBench/queries/NeuroKit_02/input/eda_analysis_01_input.csv")
sampling_rate = 100  # Assuming 100Hz sampling rate based on typical EDA recordings

# Process EDA
signals, info = nk.eda_process(data["EDA"], sampling_rate=sampling_rate)

# Plot results
nk.eda_plot(signals, info)
plt.savefig("/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/NeuroKit_02/eda_plot.png")

# Save processed data
signals.to_csv("/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/NeuroKit_02/processed_eda.csv", index=False)

# Print summary statistics
print("EDA Analysis Summary:")
print(f"Number of SCR peaks detected: {len(info['SCR_Peaks'])}")
print(f"Mean SCR amplitude: {signals['SCR_Amplitude'].mean():.2f} μS")
print(f"Mean SCR rise time: {signals['SCR_RiseTime'].mean():.2f} seconds")