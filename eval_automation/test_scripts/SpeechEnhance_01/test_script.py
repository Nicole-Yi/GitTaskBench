import os
import sys
import json
import argparse
import numpy as np
import soundfile as sf
from pesq import pesq
import datetime
from scipy import signal

def check_file_exists(file_path):
    """检查文件是否存在且非空"""
    if not os.path.exists(file_path):
        return False, f"文件不存在: {file_path}"
    if os.path.getsize(file_path) == 0:
        return False, f"文件为空: {file_path}"
    return True, ""

def resample_audio(audio, sr, target_sr=16000):
    """重采样音频到目标采样率"""
    if sr == target_sr:
        return audio
    # 计算重采样因子
    resample_factor = target_sr / sr
    # 重采样
    resampled_audio = signal.resample_poly(audio, int(len(audio) * resample_factor), len(audio))
    return resampled_audio

def check_audio_file(file_path):
    """检查音频文件格式是否正确"""
    try:
        data, sr = sf.read(file_path)
        return True, sr
    except Exception as e:
        return False, f"音频文件 {file_path} 格式错误: {str(e)}"

def calculate_metrics(enhanced_file, reference_file, pesq_threshold=2.0, snr_threshold=15.0):
    """计算 PESQ 和 SNR 指标"""
    # 检查文件
    process_ok, process_msg = check_file_exists(enhanced_file)
    if not process_ok:
        return False, False, process_msg
    
    process_ok, process_msg = check_file_exists(reference_file)
    if not process_ok:
        return False, False, process_msg
    
    # 检查音频格式
    process_ok, sr_enhanced = check_audio_file(enhanced_file)
    if not process_ok:
        return True, False, sr_enhanced
    
    process_ok, sr_reference = check_audio_file(reference_file)
    if not process_ok:
        return True, False, sr_reference

    try:
        # 读取音频文件
        enhanced, sr_enhanced = sf.read(enhanced_file)
        reference, sr_reference = sf.read(reference_file)

        # 如果是多声道，取第一个声道
        if len(enhanced.shape) > 1:
            enhanced = enhanced[:, 0]
        if len(reference.shape) > 1:
            reference = reference[:, 0]

        # 重采样到16000Hz
        enhanced = resample_audio(enhanced, sr_enhanced)
        reference = resample_audio(reference, sr_reference)

        # 确保音频长度一致
        min_len = min(len(enhanced), len(reference))
        enhanced = enhanced[:min_len]
        reference = reference[:min_len]

        # 计算 PESQ
        pesq_score = pesq(16000, reference, enhanced, 'wb')
        
        # 计算 SNR
        noise = reference - enhanced
        snr = 10 * np.log10(np.sum(reference**2) / np.sum(noise**2))

        comments = [
            f"PESQ = {pesq_score:.2f}",
            f"SNR = {snr:.2f} dB"
        ]

        result_ok = pesq_score >= pesq_threshold and snr >= snr_threshold
        if not result_ok:
            if pesq_score < pesq_threshold:
                comments.append(f"PESQ ({pesq_score:.2f}) 低于阈值 {pesq_threshold}")
            if snr < snr_threshold:
                comments.append(f"SNR ({snr:.2f} dB) 低于阈值 {snr_threshold} dB")

        return True, result_ok, "\n".join(comments)

    except Exception as e:
        return True, False, f"计算指标时出错: {str(e)}"

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
    parser = argparse.ArgumentParser(description='评估语音增强结果')
    parser.add_argument('enhanced_file', help='增强后的音频文件路径')
    parser.add_argument('reference_file', help='参考音频文件路径')
    parser.add_argument('--pesq-thresh', type=float, default=2.0, help='PESQ阈值')
    parser.add_argument('--snr-thresh', type=float, default=15.0, help='SNR阈值')
    parser.add_argument('--result', required=True, help='结果JSONL文件路径')
    
    args = parser.parse_args()
    
    process_ok, result_ok, comments = calculate_metrics(
        args.enhanced_file,
        args.reference_file,
        args.pesq_thresh,
        args.snr_thresh
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