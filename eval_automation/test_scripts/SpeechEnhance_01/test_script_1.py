#!/usr/bin/env python3
import os, sys, argparse
import numpy as np                          # numpy 运算
import soundfile as sf                      # 音频读写
from pesq import pesq                       # PESQ 计算
import json                                 # JSON处理
from datetime import datetime               # 时间处理
import pathlib                              # 路径处理

def check_file(path, exts=('.wav','.flac','.mp3')):
    if not os.path.isfile(path):
        sys.exit("错误：文件不存在 -> {}".format(path))
    if not path.lower().endswith(exts):
        sys.exit("错误：不支持的格式 -> {}".format(path))

def compute_snr(orig, proc):
    # SNR = 10 log10(E[y^2]/E[(y-x)^2])
    power_signal = np.mean(proc**2)
    noise = proc - orig
    power_noise = np.mean(noise**2)
    return 10 * np.log10(power_signal / power_noise + 1e-10)

def save_result_to_json(result, output_file="test_results.json"):
    """将测试结果保存到JSON文件"""
    # 准备数据
    data = {
        "Results": result,
        "TimePoint": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    }
    
    # 确保输出目录存在
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 检查文件是否存在
    file_path = pathlib.Path(output_file)
    
    if file_path.exists():
        # 文件存在，读取现有内容并追加
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                
            # 确保existing_data是列表
            if not isinstance(existing_data, list):
                existing_data = [existing_data]
                
            existing_data.append(data)
            result_data = existing_data
        except json.JSONDecodeError:
            # 文件存在但不是有效的JSON，创建新列表
            result_data = [data]
    else:
        # 文件不存在，创建新列表
        result_data = [data]
    
    # 保存结果
    with open(output_file, 'w', encoding='utf-8') as f:
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
    p.add_argument('--output-json', type=str, default="speech_enhance_results.json",
                   help="结果输出的JSON文件路径")
    args = p.parse_args()

    # 文件检测
    check_file(args.noisy)
    check_file(args.cleaned)

    # 读取音频
    noisy,  sr1 = sf.read(args.noisy)
    clean,  sr2 = sf.read(args.cleaned)
    if sr1 != sr2:
        sys.exit("错误：采样率不一致")
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