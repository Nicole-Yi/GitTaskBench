import argparse
import os
import json
from datetime import datetime
from io import StringIO
import sys
import difflib  # 用于计算相似度

def compute_similarity(text1, text2):
    return difflib.SequenceMatcher(None, text1, text2).ratio()

def test_watermark_extraction(extracted_txt_path, ground_truth_path, similarity_threshold=0.9):
    comments = []
    process_success = True
    result_success = False

    try:
        for path, label in [(extracted_txt_path, "提取结果"), (ground_truth_path, "Ground Truth")]:
            if not os.path.exists(path):
                comments.append(f"{label} 文件不存在：{path}")
                process_success = False
            elif os.path.getsize(path) == 0:
                comments.append(f"{label} 文件为空：{path}")
                process_success = False

        if not process_success:
            return process_success, result_success, "\n".join(comments)

        with open(extracted_txt_path, 'r', encoding='utf-8') as f:
            extracted_watermark = f.read().strip()

        with open(ground_truth_path, 'r', encoding='utf-8') as f:
            ground_truth = f.read().strip()

        similarity = compute_similarity(extracted_watermark, ground_truth)
        similarity_percent = round(similarity * 100, 2)

        if similarity == 1.0:
            result_success = True
            comments.append("✅ 水印提取成功，完全匹配！")
        elif similarity >= similarity_threshold:
            result_success = True
            comments.append(f"⚠️ 水印基本匹配，相似度 {similarity_percent}%（阈值：{int(similarity_threshold * 100)}%）")
        else:
            comments.append(f"❌ 水印提取失败，相似度 {similarity_percent}% 低于阈值（{int(similarity_threshold * 100)}%）")
            comments.append(f"解码水印: {extracted_watermark}")
            comments.append(f"Ground truth: {ground_truth}")

    except Exception as e:
        process_success = False
        comments.append(f"系统异常：{str(e)}")

    return process_success, result_success, "\n".join(comments)

def save_result_jsonl(result_path, process_flag, result_flag, comments_text):
    record = {
        "Process": process_flag,
        "Result": result_flag,
        "TimePoint": datetime.now().isoformat(timespec="seconds"),
        "comments": comments_text
    }

    try:
        with open(result_path, 'a', encoding='utf-8') as f:
            json.dump(record, f, ensure_ascii=False)
            f.write('\n')
        print(f"[✅] 成功写入 JSONL: {result_path}")
    except Exception as e:
        print(f"[❌] 写入 JSONL 失败: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="评估水印提取的准确性")
    parser.add_argument("--extracted_txt", required=True, help="提取的水印文本文件路径")
    parser.add_argument("--ground_truth_txt", required=True, help="ground truth 文本文件路径")
    parser.add_argument("--result", required=False, help="JSONL 输出路径")
    parser.add_argument("--threshold", type=float, default=0.9, help="匹配相似度阈值（默认 0.9）")
    args = parser.parse_args()

    original_stdout = sys.stdout
    buffer = StringIO()
    sys.stdout = buffer

    process_flag, result_flag, comments_text = test_watermark_extraction(
        args.extracted_txt, args.ground_truth_txt, similarity_threshold=args.threshold
    )

    sys.stdout = original_stdout
    captured_output = buffer.getvalue()
    full_comments = f"{comments_text}\n{captured_output.strip()}"

    if args.result:
        save_result_jsonl(args.result, process_flag, result_flag, full_comments)

    print(full_comments)
