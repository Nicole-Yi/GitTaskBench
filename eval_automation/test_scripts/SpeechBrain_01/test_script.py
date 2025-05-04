import os
import sys
import json
import argparse
import numpy as np
import soundfile as sf
from mir_eval.separation import bss_eval_sources
import datetime

def check_file_exists(file_path):
    """检查文件是否存在且非空"""
    if not os.path.exists(file_path):
        return False, f"文件不存在: {file_path}"
    if os.path.getsize(file_path) == 0:
        return False, f"文件为空: {file_path}"
    return True, ""

def check_audio_file(file_path):
    """检查音频文件格式是否正确"""
    try:
        data, sr = sf.read(file_path)
        # 移除单声道检查，支持多声道
        return True, ""
    except Exception as e:
        return False, f"音频文件 {file_path} 格式错误: {str(e)}"

def calculate_metrics(reference_dir, estimated_dir, snr_threshold=12.0, sdr_threshold=8.0):
    """计算 SNR 和 SDR 指标"""
    # 检查目录
    if not os.path.exists(reference_dir):
        return False, False, f"参考目录不存在: {reference_dir}"
    if not os.path.exists(estimated_dir):
        return False, False, f"估计目录不存在: {estimated_dir}"

    # 获取所有音频文件
    ref_files = sorted([f for f in os.listdir(reference_dir) if f.endswith('.wav')])
    est_files = sorted([f for f in os.listdir(estimated_dir) if f.endswith('.wav')])

    if not ref_files or not est_files:
        return True, False, "没有找到音频文件"

    # 检查文件
    for file in ref_files + est_files:
        file_path = os.path.join(reference_dir if file in ref_files else estimated_dir, file)
        process_ok, msg = check_audio_file(file_path)
        if not process_ok:
            return True, False, msg

    # 计算指标
    total_snr = 0
    total_sdr = 0
    count = 0
    comments = []

    for ref_file, est_file in zip(ref_files, est_files):
        ref_path = os.path.join(reference_dir, ref_file)
        est_path = os.path.join(estimated_dir, est_file)

        # 读取音频文件
        ref_audio, ref_sr = sf.read(ref_path)
        est_audio, est_sr = sf.read(est_path)

        # 如果是多声道，取第一个声道
        if len(ref_audio.shape) > 1:
            ref_audio = ref_audio[:, 0]
        if len(est_audio.shape) > 1:
            est_audio = est_audio[:, 0]

        # 确保音频长度一致
        min_len = min(len(ref_audio), len(est_audio))
        ref_audio = ref_audio[:min_len]
        est_audio = est_audio[:min_len]

        # 计算 SNR
        noise = ref_audio - est_audio
        snr = 10 * np.log10(np.sum(ref_audio**2) / np.sum(noise**2))
        
        # 计算 SDR
        sdr, _, _, _ = bss_eval_sources(ref_audio.reshape(1, -1), est_audio.reshape(1, -1))
        sdr = sdr[0]

        total_snr += snr
        total_sdr += sdr
        count += 1

        comments.append(f"文件 {ref_file}: SNR = {snr:.2f} dB, SDR = {sdr:.2f} dB")

    avg_snr = total_snr / count
    avg_sdr = total_sdr / count

    comments.append(f"平均 SNR = {avg_snr:.2f} dB, 平均 SDR = {avg_sdr:.2f} dB")
    
    result_ok = avg_snr >= snr_threshold and avg_sdr >= sdr_threshold
    if not result_ok:
        comments.append(f"SNR ({avg_snr:.2f} dB) 或 SDR ({avg_sdr:.2f} dB) 未达到阈值")

    return True, result_ok, "\n".join(comments)

def save_results_to_jsonl(process_ok, result_ok, comments, jsonl_file):
    """保存测试结果到JSONL文件"""
    current_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    
    result_data = {
        "Process": bool(process_ok),
        "Results": bool(result_ok),
        "TimePoint": current_time,
        "comments": comments
    }
    
    os.makedirs(os.path.dirname(jsonl_file), exist_ok=True)
    
    with open(jsonl_file, 'a', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, default=str)
        f.write('\n')

def main():
    parser = argparse.ArgumentParser(description='评估语音分离结果')
    parser.add_argument('--reference_dir', required=True, help='参考音频目录')
    parser.add_argument('--estimated_dir', required=True, help='估计音频目录')
    parser.add_argument('--snr_threshold', type=float, default=12.0, help='SNR阈值')
    parser.add_argument('--sdr_threshold', type=float, default=8.0, help='SDR阈值')
    parser.add_argument('--result', required=True, help='结果JSONL文件路径')
    
    args = parser.parse_args()
    
    process_ok, result_ok, comments = calculate_metrics(
        args.reference_dir,
        args.estimated_dir,
        args.snr_threshold,
        args.sdr_threshold
    )
    
    save_results_to_jsonl(process_ok, result_ok, comments, args.result)
    
    if not process_ok:
        print(f"处理失败: {comments}")
        sys.exit(1)
    if not result_ok:
        print(f"结果不满足要求: {comments}")
        sys.exit(1)
    print("测试通过！")

if __name__ == "__main__":
    main() 