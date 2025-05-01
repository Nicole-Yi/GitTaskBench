#!/usr/bin/env python3
import os, sys, argparse
import numpy as np                          # numpy 运算
import soundfile as sf                      # 音频读写
from pesq import pesq                       # PESQ 计算
import json                                 # JSON处理
from datetime import datetime               # 时间处理
import pathlib                              # 路径处理
from scipy import signal                    # 重采样

def check_file(path, exts=('.wav','.flac','.mp3')):
    if not os.path.isfile(path):
        sys.exit("错误：文件不存在 -> {}".format(path))
    if not path.lower().endswith(exts):
        sys.exit("错误：不支持的格式 -> {}".format(path))

def resample_audio(audio, orig_sr, target_sr=16000):
    """将音频重采样到目标采样率"""
    number_of_samples = round(len(audio) * float(target_sr) / orig_sr)
    return signal.resample(audio, number_of_samples)

def ensure_mono(audio):
    """确保音频是单声道"""
    if len(audio.shape) > 1:
        return audio.mean(axis=1)
    return audio

def ensure_float32(audio):
    """确保音频数据是float32格式"""
    if audio.dtype != np.float32:
        return audio.astype(np.float32)
    return audio

def compute_snr(orig, proc):
    # SNR = 10 log10(E[y^2]/E[(y-x)^2])
    power_signal = np.mean(proc**2)
    noise = proc - orig
    power_noise = np.mean(noise**2)
    return 10 * np.log10(power_signal / power_noise + 1e-10)

def save_result_to_json(ok, output_json):
    """保存结果到JSON文件"""
    result_data = {
        "result": bool(ok),  # 将numpy.bool_转换为Python bool
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description="评估降噪后的语音质量 (PESQ & SNR)"
    )
    p.add_argument('noisy',   help="原始含噪音频路径")
    p.add_argument('cleaned', help="降噪后音频路径")
    p.add_argument('--pesq-thresh', type=float, default=2.0,
                   help="PESQ 阈值 (≥ 阈值 则通过)")
    p.add_argument('--snr-thresh',  type=float, default=20.0,
                   help="SNR 阈值 (dB)")
    p.add_argument('--output-json', type=str, default="test_results/SpeechEnhance_01/results.json",
                   help="结果输出的JSON文件路径")
    args = p.parse_args()

    # 文件检测
    check_file(args.noisy)
    check_file(args.cleaned)

    # 读取音频
    noisy,  sr1 = sf.read(args.noisy)
    clean,  sr2 = sf.read(args.cleaned)
    print(f"采样率: noisy={sr1}, clean={sr2}")
    if sr1 != sr2:
        sys.exit("错误：采样率不一致")
    
    # 确保音频格式正确
    noisy = ensure_mono(noisy)
    clean = ensure_mono(clean)
    noisy = ensure_float32(noisy)
    clean = ensure_float32(clean)
    
    # 重采样到16000Hz
    if sr1 != 16000:
        print(f"将音频从{sr1}Hz重采样到16000Hz")
        noisy = resample_audio(noisy, sr1, 16000)
        clean = resample_audio(clean, sr2, 16000)
        sr1 = sr2 = 16000

    # 统一时长
    L = min(len(noisy), len(clean))
    noisy = noisy[:L]
    clean = clean[:L]

    # 计算指标
    pesq_score = pesq(sr1, noisy, clean, 'wb')   # wide‑band 模式
    snr_score  = compute_snr(noisy, clean)       # 相对残余噪声 SNR

    # 输出指标结果
    print("PESQ: {:.3f}".format(pesq_score))
    print("SNR:  {:.2f} dB".format(snr_score))

    # 判定
    ok = (pesq_score >= args.pesq_thresh) and (snr_score >= args.snr_thresh)
    
    # 输出最终判定结果（仅True或False）
    print(str(ok).lower())
    
    # 保存结果到JSON文件
    save_result_to_json(ok, args.output_json) 