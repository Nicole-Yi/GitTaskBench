import os
from difflib import SequenceMatcher
import argparse
import json
import datetime

def cer(ref, hyp):
    """
    计算字符错误率 CER（Character Error Rate）
    """
    matcher = SequenceMatcher(None, ref, hyp)
    edit_ops = sum(
        [max(triple[2] - triple[1], triple[2] - triple[1]) 
         for triple in matcher.get_opcodes() if triple[0] != 'equal']
    )
    return edit_ops / max(len(ref), 1)

def load_transcripts(file_path):
    """
    从文本文件加载说话人转录，格式要求：
    每一行为：speaker_id:transcript
    同一个说话人的多条记录将被合并为一个完整的字符串。
    """
    transcripts = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if ':' not in line:
                continue
            speaker, text = line.split(':', 1)
            if speaker not in transcripts:
                transcripts[speaker] = []
            transcripts[speaker].append(text)
    
    # 合并每个说话人的所有转录文本
    for speaker in transcripts:
        transcripts[speaker] = "".join(transcripts[speaker])
    
    return transcripts

def evaluate(system_output_file, ground_truth_file, cer_threshold=0.05, save_to_json=True, json_file="test_results.json"):
    """
    主评估函数：对比系统输出与标准答案，逐个说话人计算 CER
    """
    system_trans = load_transcripts(system_output_file)
    ground_truth = load_transcripts(ground_truth_file)

    total_pass = True
    results = {}

    # 遍历 ground truth 中的每个说话人
    for speaker in ground_truth:
        gt_text = ground_truth.get(speaker, "")
        sys_text = system_trans.get(speaker, "") 
        score = cer(gt_text, sys_text)
        results[speaker] = score
        if score > cer_threshold:
            total_pass = False

    # 如果需要保存到JSON文件
    if save_to_json:
        save_results_to_json(total_pass, json_file)
        
    return total_pass

def save_results_to_json(test_passed, json_file="test_results.json"):
    """
    保存测试结果到JSON文件
    """
    # 获取当前时间
    current_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    
    # 准备要保存的数据
    result_data = {
        "Results": test_passed,
        "TimePoint": current_time
    }
    
    # 创建目录（如果不存在）
    os.makedirs(os.path.dirname(json_file), exist_ok=True)
    
    # 检查文件是否存在
    if os.path.exists(json_file):
        # 读取现有内容
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                if not isinstance(existing_data, list):
                    existing_data = [existing_data]
        except (json.JSONDecodeError, FileNotFoundError):
            existing_data = []
    else:
        existing_data = []
    
    # 添加新结果
    existing_data.append(result_data)
    
    # 保存到文件
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)

def parse_args():
    parser = argparse.ArgumentParser(description="评估ASR系统对不同说话人的转录准确率（基于CER）")
    parser.add_argument('--system_output', type=str, required=True,
                        help='系统输出的转录文件路径（每行格式为 speaker_id:transcript）')
    parser.add_argument('--ground_truth', type=str, required=True,
                        help='标准答案的转录文件路径（每行格式为 speaker_id:transcript）')
    parser.add_argument('--cer_threshold', type=float, default=0.05,
                        help='CER 阈值，默认值为 0.05')
    parser.add_argument('--json_file', type=str, default="test_results.json",
                        help='保存结果的JSON文件路径')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    # 设置默认的结果保存路径为test_results/FunASR_01/results.json
    default_results_file = "test_results/FunASR_01/results.json"
    json_file = args.json_file if args.json_file != "test_results.json" else default_results_file
    
    result = evaluate(args.system_output, args.ground_truth, 
                      cer_threshold=args.cer_threshold,
                      json_file=json_file)
    # 只输出True或False
    print(result) 