import torch
from TTS.utils.audio import AudioProcessor
from TTS.utils.synthesizer import Synthesizer

def test_tts(model_path, config_path, output_path, text):
    synthesizer = Synthesizer(
        tts_checkpoint=model_path,
        tts_config_path=config_path,
        use_cuda=torch.cuda.is_available()
    )
    
    wav = synthesizer.tts(text)
    synthesizer.save_wav(wav, output_path)
    print(f"Audio saved to {output_path}")

if __name__ == "__main__":
    model_path = "tts_output/best_model.pth"
    config_path = "tts_output/config.json"
    output_path = "test_output.wav"
    text = "This is a test of the fine-tuned text-to-speech model."
    test_tts(model_path, config_path, output_path, text)
