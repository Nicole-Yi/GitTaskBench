import torch
import torchaudio
from speechbrain.pretrained import SpectralMaskEnhancement
from speechbrain.pretrained import EncoderDecoderASR

def process_audio(input_path, output_path):
    # 1. Load the audio file
    waveform, sample_rate = torchaudio.load(input_path)
    
    # 2. Initialize the enhancement model
    enhancer = SpectralMaskEnhancement.from_hparams(
        source="speechbrain/metricgan-plus-voicebank",
        savedir="pretrained_models/metricgan-plus-voicebank"
    )
    
    # 3. Enhance the audio
    enhanced = enhancer.enhance_batch(waveform, lengths=torch.tensor([1.]))
    
    # 4. Save the enhanced audio
    torchaudio.save(output_path + "_enhanced.wav", enhanced.cpu(), sample_rate)
    
    # 5. Initialize the ASR model
    asr_model = EncoderDecoderASR.from_hparams(
        source="speechbrain/asr-conformer-transformerlm-librispeech",
        savedir="pretrained_models/asr-conformer-transformerlm-librispeech"
    )
    
    # 6. Perform speech recognition on both original and enhanced audio
    original_text = asr_model.transcribe_file(input_path)
    enhanced_text = asr_model.transcribe_file(output_path + "_enhanced.wav")
    
    # 7. Save transcription results
    with open(output_path + "_transcription.txt", "w") as f:
        f.write("Original Audio Transcription:\n")
        f.write(original_text + "\n\n")
        f.write("Enhanced Audio Transcription:\n")
        f.write(enhanced_text + "\n")

if __name__ == "__main__":
    input_path = "/data/data/agent_test_codebase/GitTaskBench/queries/SpeechBrain_01/input/SpeechBrain_01_input.wav"
    output_path = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/SpeechBrain_01/output"
    process_audio(input_path, output_path)