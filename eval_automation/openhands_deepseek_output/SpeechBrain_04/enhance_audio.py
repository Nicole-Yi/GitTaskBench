from speechbrain.inference.separation import SepformerSeparation as separator
import torchaudio

# Load pretrained model
model = separator.from_hparams(
    source="speechbrain/sepformer-whamr-enhancement",
    savedir="/tmp/sepformer-whamr-enhancement"
)

# Process input file
enhanced_speech = model.separate_file(
    path="/data/data/agent_test_codebase/GitTaskBench/queries/SpeechBrain_04/input/SpeechBrain_04_input.wav"
)

# Save enhanced audio
torchaudio.save(
    "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/SpeechBrain_04/output.wav",
    enhanced_speech[:, :, 0].detach().cpu(),
    16000  # Assuming sample rate of 16000
)

print("Speech enhancement completed. Output saved to output.wav")