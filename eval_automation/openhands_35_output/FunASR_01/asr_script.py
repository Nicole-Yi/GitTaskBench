from funasr import AutoModel

# 输入和输出文件路径
input_file = "/data/data/agent_test_codebase/GitTaskBench/queries/FunASR_01/input/FunASR_01_input.wav"
output_file = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/FunASR_01/output.txt"

# 初始化模型
model = AutoModel(
    model="damo/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch",
    model_revision="v2.0.4",
)

# 执行语音识别
results = model.generate(input=input_file)

# 保存结果到文件
with open(output_file, 'w', encoding='utf-8') as f:
    for item in results:
        text = item["text"]
        timestamp = item.get("timestamp", [])  # 获取时间戳信息（如果有）
        
        # 写入识别文本
        f.write(f"文本: {text}\n")
        
        # 如果有时间戳信息，也写入文件
        if timestamp:
            f.write(f"时间戳: {timestamp}\n")
        
        f.write("\n")  # 添加空行分隔不同的识别结果

print(f"语音识别结果已保存到: {output_file}")