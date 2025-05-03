import torch
import torchaudio
from speechbrain.pretrained import EncoderClassifier

def transcribe_audio(input_path, output_path):
    # Initialize the model
    classifier = EncoderClassifier.from_hparams(
        source="speechbrain/spkrec-xvect-voxceleb",
        savedir="pretrained_models/spkrec-xvect-voxceleb"
    )
    
    # Load and process audio
    signal, fs = torchaudio.load(input_path)
    embeddings = classifier.encode_batch(signal)
    
    # Save embeddings
    torch.save(embeddings, output_path + "_embeddings.pt")
    
    # Save a simple text file indicating completion
    with open(output_path + "_processed.txt", "w") as f:
        f.write("Audio processing completed.\n")
        f.write(f"Embeddings shape: {embeddings.shape}\n")

if __name__ == "__main__":
    input_path = "/data/data/agent_test_codebase/GitTaskBench/queries/SpeechBrain_01/input/SpeechBrain_01_input.wav"
    output_path = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/SpeechBrain_01/output"
    transcribe_audio(input_path, output_path)