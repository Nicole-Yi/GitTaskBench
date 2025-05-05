import argparse
import json
import os
from datetime import datetime

def evaluate(pred_path, gt_path, result_path):
    """直接按文本字符重复度评估"""
    threshold = 0.80  # 成功门槛

    # 读入两个文本
    if not os.path.isfile(pred_path) or not os.path.isfile(gt_path):
        print("❌ 输入文件不存在！")
        return False

    with open(pred_path, "r", encoding="utf-8") as f:
        pred_text = f.read().lower().replace(" ", "").replace("\n", "")
    with open(gt_path, "r", encoding="utf-8") as f:
        gt_text = f.read().lower().replace(" ", "").replace("\n", "")

    # 计算字符级别的重合率
    common = sum((1 for c1, c2 in zip(pred_text, gt_text) if c1 == c2))
    max_len = max(len(pred_text), len(gt_text))
    similarity = common / max_len if max_len else 0

    # 获取当前时间并格式化为 ISO 8601 格式
    time_point = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    # 构建结果字典
    result = {
        "Process": True,
        "Result": similarity >= threshold,  # 改为单数形式并直接计算布尔值
        "TimePoint": time_point,
        "comments": f"文本相似度={similarity:.4f} (阈值={threshold})"
    }

    # 处理测试结果
    if result["Result"]:
        print(f"✅ 测试通过！{result['comments']}")
    else:
        print(f"❌ 测试未通过。{result['comments']}")

    # 确保结果目录存在
    os.makedirs(os.path.dirname(result_path) or '.', exist_ok=True)

    # 将结果写入 JSONL 文件
    try:
        with open(result_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')
    except Exception as e:
        print(f"❌ 写入结果失败: {e}")
        return False

    return True

def main():
    parser = argparse.ArgumentParser(description="Evaluate text similarity between predicted and ground truth texts.")
    parser.add_argument("--pred", required=True, help="Predicted output file path")
    parser.add_argument("--gt", required=True, help="Ground truth file path")
    parser.add_argument("--result", required=True, help="Path to save the result JSONL file")
    args = parser.parse_args()

    success = evaluate(args.pred, args.gt, args.result)

    if not success:
        print("❌ 测试执行失败，请检查日志")
        exit(1)
    else:
        print(f"✅ 测试完成，结果已保存到: {args.result}")

if __name__ == "__main__":
    main()