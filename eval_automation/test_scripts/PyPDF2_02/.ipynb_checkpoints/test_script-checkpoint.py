import argparse
import os
import json
import datetime
from pypdf import PdfReader
import glob

def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text.replace("\n", "").replace(" ", "")
    except Exception as e:
        return f"[ERROR] {str(e)}"

def evaluate(split_dir, truth_dir, result_path):
    log = {
        "Process": True,
        "Result": False,
        "TimePoint": datetime.datetime.now().isoformat(),
        "comments": ""
    }

    try:
        split_files = sorted(glob.glob(os.path.join(split_dir, "**", "*.pdf"), recursive=True))
        truth_files = sorted(glob.glob(os.path.join(truth_dir, "**", "*.pdf"), recursive=True))

        if not split_files:
            log["Process"] = False
            log["comments"] += "❌ 拆分目录中没有 .pdf 文件 "
        if not truth_files:
            log["Process"] = False
            log["comments"] += "❌ 标准目录中没有 .pdf 文件 "

        if not log["Process"]:
            write_result(result_path, log)
            return

        if len(split_files) != len(truth_files):
            log["comments"] += f"❌ 拆分页数不一致！split: {len(split_files)}, truth: {len(truth_files)} "
            write_result(result_path, log)
            return

        total_pages = len(truth_files)
        passed_pages = 0
        page_logs = []

        for split_file, truth_file in zip(split_files, truth_files):
            split_text = extract_text_from_pdf(split_file)
            truth_text = extract_text_from_pdf(truth_file)

            if isinstance(split_text, str) and split_text.startswith("[ERROR]"):
                page_logs.append(f"❌ 读取 {split_file} 出错：{split_text}")
                continue
            if isinstance(truth_text, str) and truth_text.startswith("[ERROR]"):
                page_logs.append(f"❌ 读取 {truth_file} 出错：{truth_text}")
                continue

            if not truth_text:
                page_logs.append(f"⚠️ Ground truth {os.path.basename(truth_file)} 为空，跳过")
                continue

            correct_chars = sum(1 for a, b in zip(split_text, truth_text) if a == b)
            accuracy = (correct_chars / len(truth_text)) * 100

            if accuracy >= 95:
                passed_pages += 1
            else:
                page_logs.append(f"❌ {os.path.basename(split_file)} 内容准确率仅 {accuracy:.2f}%")

        if passed_pages == total_pages:
            log["Result"] = True
            log["comments"] += f"✅ 所有 {total_pages} 页均成功拆分且准确率 >= 95%"
        else:
            log["comments"] += f"❌ 有 {total_pages - passed_pages} 页未达到准确率要求\n" + "\n".join(page_logs)

    except Exception as e:
        log["Process"] = False
        log["comments"] += f"[异常错误] {str(e)}"

    write_result(result_path, log)

def write_result(result_path, log):
    os.makedirs(os.path.dirname(result_path), exist_ok=True)
    with open(result_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(log, ensure_ascii=False, default=str) + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--split_dir", type=str, required=True, help="拆分后页面文件夹路径")
    parser.add_argument("--truth_dir", type=str, required=True, help="标准答案页面文件夹路径")
    parser.add_argument("--result", type=str, required=True, help="结果写入的 JSONL 路径")
    args = parser.parse_args()

    evaluate(args.split_dir, args.truth_dir, args.result)
