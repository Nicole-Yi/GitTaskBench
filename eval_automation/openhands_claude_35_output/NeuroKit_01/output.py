import neurokit2 as nk
import pandas as pd
import matplotlib.pyplot as plt

# 读取ECG数据
input_file = "/data/data/agent_test_codebase/GitTaskBench/queries/NeuroKit_01/input/ecg_hrv_analysis_01_input.csv"
data = pd.read_csv(input_file)
ecg_signal = data['ECG'].values
sampling_rate = 250  # 假设采样率为250Hz，如果实际不同请调整

# 处理ECG信号
signals, info = nk.ecg_process(ecg_signal, sampling_rate=sampling_rate)

# 计算HRV指标
hrv_indices = nk.hrv(info["ECG_R_Peaks"], sampling_rate=sampling_rate, show=True)

# 保存HRV指标
hrv_indices.to_csv("/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/NeuroKit_01/output_hrv.csv")

# 生成ECG处理结果的可视化
plt.figure(figsize=(15, 6))
nk.ecg_plot(signals, info)
plt.savefig("/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/NeuroKit_01/output_ecg_plot.png")
plt.close()

