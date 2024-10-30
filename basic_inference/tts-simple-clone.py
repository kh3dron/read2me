import os
from pydub import AudioSegment
import torch
from TTS.api import TTS

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"


# clones
model = "tts_models/multilingual/multi-dataset/xtts_v2"

# 4s of gibberish appended to start of each sentence
# model = "tts_models/en/ljspeech/vits"

# moaning
# model = "tts_models/en/ljspeech/tacotron2-DDC"

# model = "tts_models/en/ljspeech/tacotron2-DDC_ph"



tts = TTS(model).to(device)

textfile = "../data/text/fountainhead.txt"
note = "xtts_v2"

speaker = "steve_jobs"
source = "../data/audio/steve_jobs/full_mono.wav"

text_dir = f"../data/text/{textfile}"
# output_file = f"../output_audio/{textfile}-{speaker}-{note}"
output_file = "test.wav"


with open(textfile, "r", encoding="utf-8") as file:
    text_content = file.read()


tts.tts_to_file(
    text=text_content,
    speaker_wav=source,
    # voice_dir=source,
    # speaker=speaker,
    file_path=output_file,
    language="en"
)

