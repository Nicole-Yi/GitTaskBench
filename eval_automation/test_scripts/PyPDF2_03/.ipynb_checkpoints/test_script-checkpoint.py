import argparse
import json
from datetime import datetime

def load_metadata(file_path):
    metadata = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if ": " in line:
                key, value = line.strip().split(": ", 1)
                metadata[key] = value
    return metadata

def evaluate(pred_file, truth_file, result_file):
    pred_metadata = load_metadata(pred_file)
    truth_metadata = load_metadata(truth_file)

    total_fields = len(truth_metadata)
    correct_fields = 0
    comments = []

    for key, truth_value in truth_metadata.items():
        pred_value = pred_metadata.get(key)
        if pred_value == truth_value:
            correct_fields += 1
        else:
            comments.append(f"❌ 字段 {key} 不匹配：预测是 {pred_value}，正确是 {truth_value}")

    accuracy = (correct_fields / total_fields) * 100
    comments.append(f"🎯 字段级准确率: {accuracy:.2f}%")

    if accuracy == 100:
        comments.append("✅ 测试通过！")
        result = True
    else:
        comments.append("❌ 测试未通过")
        result = False

    # 打印评论
    for comment in comments:
        print(comment)

    # 获取当前时间戳
    time_point = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    # 创建结果对象
    result_data = {
        "Process": True,
        "Results": result,
        "TimePoint": time_point,
        "comments": " ".join(comments)
    }

    # 保存到 jsonl 文件
    with open(result_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(result_data, default=str) + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pred_file", type=str, required=True, help="提取的元信息文件路径")
    parser.add_argument("--truth_file", type=str, required=True, help="标准元信息文件路径")
    parser.add_argument("--result", type=str, required=True, help="结果保存的 jsonl 文件路径")
    args = parser.parse_args()

    evaluate(args.pred_file, args.truth_file, args.result)
