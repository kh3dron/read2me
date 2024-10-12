import torch
from TTS.api import TTS

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# List available 🐸TTS models
print(TTS().list_models())


model = "tts_models/multilingual/multi-dataset/xtts_v2"  # clones

# model = "tts_models/en/ljspeech/tacotron2-DDC" # fail to clone
# model = "tts_models/en/ljspeech/tacotron2-DDC_ph" # fail to clone

# Init TTS
tts = TTS(model).to(device)

speaker = "steve_jobs"
source = "../data/audio/steve_jobs/full_mono.wav"
text = "../data/text/fountainhead.txt"

# Read the contents of the text file
with open(text, 'r', encoding='utf-8') as file:
    text_content = file.read()

# Use the text content in the TTS function
filename = "test.wav"

tts.tts_to_file(
    text=text_content,
    speaker_wav=source,
    # voice_dir=source,
    language="en",
    # speaker=speaker,
    file_path=filename,
)