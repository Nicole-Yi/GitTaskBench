
from funasr_onnx import Paraformer
from pathlib import Path
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

model_dir = "damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch"
model = Paraformer(model_dir, batch_size=1, quantize=False)

result = model([input_file])
print(result)

with open(output_file, 'w', encoding='utf-8') as f:
    if isinstance(result, list):
        for item in result:
            if isinstance(item, dict) and 'text' in item:
                f.write(item['text'] + '\n')
            else:
                f.write(str(item) + '\n')
    else:
        f.write(str(result))
