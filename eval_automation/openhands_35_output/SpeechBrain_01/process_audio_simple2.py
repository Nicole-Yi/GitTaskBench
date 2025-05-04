import torch
import soundfile as sf
from speechbrain.pretrained import EncoderASR

def transcribe_audio(input_path, output_path):
    # Load the audio file
    waveform, sample_rate = sf.read(input_path)
    waveform = torch.tensor(waveform)
    if len(waveform.shape) == 2:
        waveform = waveform.mean(dim=1)  # Convert stereo to mono
    
    # Initialize the ASR model
    asr_model = EncoderASR.from_hparams(
        source="speechbrain/asr-wav2vec2-commonvoice-en",
        savedir="pretrained_models/asr-wav2vec2-commonvoice-en"
    )
    
    # Save waveform to a temporary file that torchaudio can read
    sf.write(output_path + "_temp.wav", waveform.numpy(), sample_rate)
    
    # Perform speech recognition
    text = asr_model.transcribe_file(output_path + "_temp.wav")
    
    # Save transcription results
    with open(output_path + "_transcription.txt", "w") as f:
        f.write("Audio Transcription:\n")
        f.write(text + "\n")

if __name__ == "__main__":
    input_path = "/data/data/agent_test_codebase/GitTaskBench/queries/SpeechBrain_01/input/SpeechBrain_01_input.wav"
    output_path = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/SpeechBrain_01/output"
    transcribe_audio(input_path, output_path)