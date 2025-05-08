import torchaudio
from speechbrain.pretrained import EncoderDecoderASR

def transcribe_audio(input_path, output_path):
    # Initialize the ASR model
    asr_model = EncoderDecoderASR.from_hparams(
        source="speechbrain/asr-transformer-transformerlm-librispeech",
        savedir="pretrained_models/asr-transformer-transformerlm-librispeech"
    )
    
    # Perform speech recognition
    text = asr_model.transcribe_file(input_path)
    
    # Save transcription results
    with open(output_path + "_transcription.txt", "w") as f:
        f.write("Audio Transcription:\n")
        f.write(text + "\n")

if __name__ == "__main__":
    input_path = "/data/data/agent_test_codebase/GitTaskBench/queries/SpeechBrain_01/input/SpeechBrain_01_input.wav"
    output_path = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/SpeechBrain_01/output"
    transcribe_audio(input_path, output_path)