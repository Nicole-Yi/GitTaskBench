#!/usr/bin/env python3
"""
评估脚本，用于评估VideoPose3D输出数据是否正确
"""

import os
import sys
import argparse
import numpy as np
import json
import datetime

def parse_args():
    parser = argparse.ArgumentParser(description='VideoPose3D输出评估')
    parser.add_argument('--input', type=str, default='output/VideoPose3D_01/output_3d.npz.npy', 
                        help='输入3D关键点文件路径')
    parser.add_argument('--result', type=str, default='test_results/VideoPose3D_01/results.jsonl',
                        help='评估结果的jsonl文件路径')
    return parser.parse_args()

def load_data(file_path):
    """加载3D关键点数据"""
    try:
        data = np.load(file_path, allow_pickle=True)
        return data
    except Exception as e:
        print(f"加载数据出错: {e}")
        return None

def evaluate_data(data):
    """评估3D关键点数据的质量"""
    results = {}
    
    # 检查数据形状
    shape = data.shape
    results['shape'] = shape
    
    # 检查数据类型
    results['dtype'] = str(data.dtype)
    
    # 检查是否有NaN值
    results['has_nan'] = np.isnan(data).any()
    
    # 基本统计信息
    results['min'] = float(np.min(data))
    results['max'] = float(np.max(data))
    results['mean'] = float(np.mean(data))
    results['std'] = float(np.std(data))
    
    # 检查连续性 - 计算相邻帧之间的平均位移
    frame_diffs = np.sqrt(np.sum(np.square(data[1:] - data[:-1]), axis=(1, 2))) if data.shape[0] > 1 else np.array([])
    
    if frame_diffs.size > 0:
        results['avg_frame_diff'] = float(np.mean(frame_diffs))
        results['max_frame_diff'] = float(np.max(frame_diffs))
    else:
        results['avg_frame_diff'] = 0.0
        results['max_frame_diff'] = 0.0
    
    # 检查骨骼长度一致性 - 我们期望骨骼长度在各帧之间保持相对稳定
    limbs = [
        (0, 1),  # 头到颈部
        (1, 2), (2, 3),  # 右臂
        (1, 4), (4, 5),  # 左臂
        (0, 6), (6, 7),  # 躯干
        (7, 8), (8, 9),  # 右腿
        (7, 10), (10, 11)  # 左腿
    ]
    
    bone_lengths = []
    for joint1, joint2 in limbs:
        if joint1 < data.shape[1] and joint2 < data.shape[1]:
            # 计算骨骼长度
            bone_vec = data[:, joint1, :] - data[:, joint2, :]
            lengths = np.sqrt(np.sum(np.square(bone_vec), axis=1))
            # 计算每个骨骼长度的变异系数(CV) = 标准差/平均值
            cv = np.std(lengths) / np.mean(lengths) if np.mean(lengths) != 0 else 0
            bone_lengths.append((joint1, joint2, float(cv)))
    
    results['bone_length_stability'] = bone_lengths
    
    # 整体评分（0-100分）
    score = 100.0
    
    # 如果有NaN值，扣20分
    if results['has_nan']:
        score -= 20
    
    # 如果骨骼长度变异系数大，扣分
    avg_cv = np.mean([cv for _, _, cv in bone_lengths])
    if avg_cv > 0.1:  # 10%以上的变异被认为是不稳定的
        score -= min(30, avg_cv * 100)  # 最多扣30分
    
    # 如果相邻帧差异过大，扣分
    if results['max_frame_diff'] > 1.0:  # 阈值需要根据实际数据调整
        score -= min(20, results['max_frame_diff'] * 10)
    
    results['score'] = max(0, score)
    
    return results


def save_results_to_jsonl(process_status, test_passed, comments, result_file):
    """
    将评估结果保存到jsonl文件
    """
    # 确保目录存在
    os.makedirs(os.path.dirname(result_file), exist_ok=True)
    
    # 获取当前时间
    current_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    
    # 准备要保存的数据
    result_data = {
        "Process": process_status,
        "Result": test_passed,
        "TimePoint": current_time,
        "comments": comments
    }
    
    # 以追加模式写入jsonl文件
    with open(result_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(result_data, ensure_ascii=False, default=str) + '\n')
    
    print(f"评估结果已写入: {result_file}")

def main():
    args = parse_args()
    
    # 检查输入文件是否存在
    if not os.path.exists(args.input):
        print(f"错误: 输入文件 {args.input} 不存在")
        comments = f"错误: 输入文件 {args.input} 不存在"
        save_results_to_jsonl(False, False, comments, args.result)
        return 1
    
    # 加载数据
    data = load_data(args.input)
    if data is None:
        comments = f"错误: 无法加载输入文件 {args.input}"
        save_results_to_jsonl(False, False, comments, args.result)
        return 1
    
    # 处理 .npz 文件：提取其中一个数组（你可以根据实际情况指定名称）
    if isinstance(data, np.lib.npyio.NpzFile):
        if len(data.files) == 0:
            comments = f"错误: 输入文件 {args.input} 中没有任何数组"
            save_results_to_jsonl(False, False, comments, args.result)
            return 1
        first_key = data.files[0]
        data = data[first_key]

    # === 添加兼容 shape ===
    # 如果是形如 (1, 1, joints, 3)，转为 (1, joints, 3)
    if len(data.shape) == 4 and data.shape[0] == 1 and data.shape[1] == 1 and data.shape[3] == 3:
        data = data[0, 0]  # -> (17, 3)
        data = data[np.newaxis, ...]  # -> (1, 17, 3)


    # 检查数据格式
    if len(data.shape) != 3 or data.shape[2] != 3:
        comments = f"错误: 输入文件格式不正确，预期形状为(frames, joints, 3)，但实际为{data.shape}"
        save_results_to_jsonl(False, False, comments, args.result)
        return 1
        
    print(f"数据形状: {data.shape}")
    
    # 评估数据
    results = evaluate_data(data)
    
    # 输出总体评分
    print(f"评估完成! 总体评分: {results['score']:.2f}/100")
    test_passed = results['score'] >= 60
    
    comments = f"评估完成! 总体评分: {results['score']:.2f}/100。"
    if test_passed:
        comments += "结果: 通过 ✅"
        print("结果: 通过 ✅")
    else:
        comments += "结果: 不通过 ❌"
        print("结果: 不通过 ❌")
    
    # 保存结果到jsonl文件
    save_results_to_jsonl(True, test_passed, comments, args.result)
    
    return 0 if test_passed else 1

if __name__ == "__main__":
    sys.exit(main()) 