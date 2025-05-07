import argparse
import jieba
import re
import json
from jiwer import wer, compute_measures
import Levenshtein
from datetime import datetime
import os

def parse_args():
    """解析命令行参数，获取输出文件、ground truth 文件、结果文件路径和 WER 阈值"""
    parser = argparse.ArgumentParser(description="评估 FunASR 输出与 ground truth 的文本相似度")
    parser.add_argument('--output', default='output.txt', help='FunASR 输出文件路径')
    parser.add_argument('--groundtruth', default='gt.txt', help='Ground truth 文件路径')
    parser.add_argument('--result', default='eval_results.jsonl', help='评估结果保存的 JSONL 文件路径')
    parser.add_argument('--wer_threshold', type=float, default=0.3, help='WER 阈值，低于此值任务视为成功')
    return parser.parse_args()

def preprocess_text(text):
    """预处理文本：移除标点和空格，使用 jieba 分词"""
    text = re.sub(r'[^\w\s]', '', text)
    text = text.replace(" ", "")
    return " ".join(jieba.cut(text))

def load_text(file_path, is_output=False):
    """加载文本文件，is_output=True 时提取 FunASR 的 text 字段"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                raise ValueError(f"文件 {file_path} 为空")
            
            if is_output:
                match = re.search(r"'text':\s*'([^']*)'", content)
                if match:
                    return preprocess_text(match.group(1)), True
                else:
                    raise ValueError(f"无法从 {file_path} 提取 text 字段")
            else:
                return preprocess_text(content), True
    except FileNotFoundError:
        return "", False
    except Exception as e:
        return "", False

def evaluate(output_file, gt_file, result_file, wer_threshold):
    """评估输出文件与 ground truth，使用 WER 和 Levenshtein 距离，并保存结果到 JSONL"""
    # 初始化日志和结果
    comments = []
    process_success = False
    result_success = False

    # 加载并预处理文本
    output_text, output_valid = load_text(output_file, is_output=True)
    gt_text, gt_valid = load_text(gt_file, is_output=False)

    # 检查文件有效性
    if output_valid and gt_valid and output_text and gt_text:
        process_success = True
        comments.append("输入文件存在、非空且格式正确")
    else:
        comments.append("输入文件存在问题：")
        if not output_valid:
            comments.append(f"输出文件 {output_file} 不存在或格式错误")
        if not gt_valid:
            comments.append(f"Ground truth 文件 {gt_file} 不存在或格式错误")
        if not output_text or not gt_text:
            comments.append("无法加载有效文本")

    # 计算评估指标（仅在文件有效时）
    wer_score = None
    normalized_lev = None
    insertions = None
    deletions = None
    substitutions = None

    if process_success:
        try:
            # 计算 WER 和详细错误统计
            measures = compute_measures(gt_text, output_text)
            wer_score = measures['wer']
            insertions = measures['insertions']
            deletions = measures['deletions']
            substitutions = measures['substitutions']

            # 计算归一化 Levenshtein 距离
            lev_distance = Levenshtein.distance(output_text.replace(" ", ""), gt_text.replace(" ", ""))
            max_len = max(len(gt_text.replace(" ", "")), len(output_text.replace(" ", "")))
            normalized_lev = lev_distance / max_len if max_len > 0 else 0

            # 记录评估结果
            comments.append(f"词错误率 (WER): {wer_score:.4f}")
            comments.append(f"归一化 Levenshtein 距离: {normalized_lev:.4f}")
            comments.append(f"插入错误数: {insertions}")
            comments.append(f"删除错误数: {deletions}")
            comments.append(f"替换错误数: {substitutions}")

            # 判断任务是否成功
            result_success = wer_score <= wer_threshold
            comments.append(f"任务{'成功完成' if result_success else '失败'}（WER {'低于' if result_success else '高于'}阈值 {wer_threshold}）")
        except Exception as e:
            comments.append(f"评估过程中发生异常: {str(e)}")
    else:
        comments.append("由于输入文件无效，未进行评估")

    # 输出到控制台
    for comment in comments:
        print(comment)

    # 保存结果到 JSONL
    result_entry = {
        "Process": process_success,
        "Result": result_success,
        "TimePoint": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "comments": "; ".join(comments)
    }

    try:
        with open(result_file, 'a', encoding='utf-8') as f:
            json.dump(result_entry, f, ensure_ascii=False, default=str)
            f.write('\n')
    except Exception as e:
        print(f"错误：无法保存结果到 {result_file} - {str(e)}")

if __name__ == "__main__":
    # 解析命令行参数
    args = parse_args()
    # 运行评估
    evaluate(args.output, args.groundtruth, args.result, args.wer_threshold)