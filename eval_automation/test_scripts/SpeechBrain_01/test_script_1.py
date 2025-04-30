import os
import numpy as np
import argparse
import soundfile as sf
import json
import datetime
from mir_eval.separation import bss_eval_sources

# 计算 SNR
def calculate_snr(ref, est):
    noise = ref - est
    snr = 10 * np.log10(np.sum(ref ** 2) / np.sum(noise ** 2) + 1e-8)
    return snr

# 计算 SDR
def calculate_sdr(ref, est):
    sdr, _, _, _ = bss_eval_sources(ref[np.newaxis, :], est[np.newaxis, :])
    return sdr[0]

# 读取语音文件
def load_audio(path):
    data, sr = sf.read(path)
    if data.ndim > 1:
        data = np.mean(data, axis=1)  # 转为单通道
    return data

# 将结果保存到JSON文件
def save_result_to_json(result, json_path="test_results.json"):
    # 获取当前时间
    time_now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    
    # 准备写入的数据
    data_to_save = {
        "Results": result,
        "TimePoint": time_now
    }
    
    # 检查文件是否存在
    all_results = []
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            try:
                all_results = json.load(f)
                if not isinstance(all_results, list):
                    all_results = [all_results]
            except json.JSONDecodeError:
                all_results = []
    
    # 添加新结果
    all_results.append(data_to_save)
    
    # 写入文件
    with open(json_path, 'w') as f:
        json.dump(all_results, f, indent=2)

# 执行评估
def evaluate(reference_dir, estimated_dir, snr_threshold=12.0, sdr_threshold=8.0, json_path="test_results.json"):
    all_pass = True
    results = []

    for filename in os.listdir(reference_dir):
        if not filename.endswith(".wav"):
            continue

        ref_path = os.path.join(reference_dir, filename)
        est_path = os.path.join(estimated_dir, filename)

        if not os.path.exists(est_path):
            print(":x: 缺失文件：{}".format(est_path))
            all_pass = False
            continue

        ref = load_audio(ref_path)
        est = load_audio(est_path)

        min_len = min(len(ref), len(est))
        ref, est = ref[:min_len], est[:min_len]

        snr = calculate_snr(ref, est)
        sdr = calculate_sdr(ref, est)

        passed = snr >= snr_threshold and sdr >= sdr_threshold
        all_pass = all_pass and passed

        results.append((filename, snr, sdr, passed))

    # 打印详细结果（可选择性注释或删除）
    print("\n=== 语音分离与降噪评估报告 ===")
    for fname, snr, sdr, ok in results:
        status = ':white_check_mark: 通过' if ok else ':x: 不通过'
        print("{}:\tSNR={:.2f} dB\tSDR={:.2f} dB\t{}".format(fname, snr, sdr, status))

    # 只输出最终结果
    print(all_pass)
    
    # 保存结果到JSON文件
    save_result_to_json(all_pass, json_path)
    
    return all_pass

# 命令行参数
def parse_args():
    parser = argparse.ArgumentParser(description="语音分离与降噪质量评估脚本")
    parser.add_argument('--reference_dir', type=str, required=True,
                        help='参考纯净语音文件目录（每位说话人分离的GT）')
    parser.add_argument('--estimated_dir', type=str, required=True,
                        help='系统输出的分离语音目录（与GT按文件名对齐）')
    parser.add_argument('--snr_threshold', type=float, default=12.0,
                        help='SNR阈值，默认12 dB')
    parser.add_argument('--sdr_threshold', type=float, default=8.0,
                        help='SDR阈值，默认8 dB')
    parser.add_argument('--json_path', type=str, default="test_results.json",
                        help='保存测试结果的JSON文件路径')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    evaluate(args.reference_dir, args.estimated_dir, args.snr_threshold, args.sdr_threshold, args.json_path) 