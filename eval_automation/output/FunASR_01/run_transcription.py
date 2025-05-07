
from funasr import AutoModel

input_audio = "/data/data/agent_test_codebase/GitTaskBench/queries/FunASR_01/input/FunASR_01_input.wav"
output_text = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/FunASR_01/output.txt"

model = AutoModel(
    model="Whisper-large-v3-turbo",
    vad_model="iic/speech_fsmn_vad_zh-cn-16k-common-pytorch",
    vad_kwargs={"max_single_segment_time": 30000},
)

DecodingOptions = {
    "task": "transcribe",
    "language": None,
    "beam_size": None,
    "fp16": True,
    "without_timestamps": False,
    "prompt": None,
}
res = model.generate(
    DecodingOptions=DecodingOptions,
    batch_size_s=0,
    input=input_audio,
)

with open(output_text, 'w') as out_file:
    out_file.write(res)

print("Transcription complete. Output saved to output.txt.")