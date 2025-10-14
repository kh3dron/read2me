import os
from pydub import AudioSegment
import torch
from TTS.api import TTS
import sys
import json

with open("speakers.json", "r") as f:
    speakers = json.load(f)

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"
model = "tts_models/multilingual/multi-dataset/xtts_v2"
tts = TTS(model).to(device)

input_text = "One hen, Two ducks, Three squawking geese, Four limerick oysters, Five corpulent porpoises, Six pairs of Don Alverzo's tweezers, Seven thousand Macedonians in full battle array"

for name in speakers["xtts_v2"]:
    tts.tts_to_file(
        text=input_text,
        file_path=f"../voice_samples/{name}.wav",
        speaker=name,
        language="en",
        split_sentences=True,
    )