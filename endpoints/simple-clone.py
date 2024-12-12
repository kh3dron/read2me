import os
from pydub import AudioSegment
import torch
from TTS.api import TTS
import sys

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"
model = "tts_models/multilingual/multi-dataset/xtts_v2"
tts = TTS(model).to(device)

if len(sys.argv) < 3:
    print("Usage: python clone-api.py <source_clip> <input_text>")
    sys.exit(1)

source_clip = sys.argv[1]
input_text = sys.argv[2]
task_id = sys.argv[3]
output_file = f"output/{task_id}.wav"

tts.tts_to_file(
    text=input_text,
    speaker_wav=source_clip,
    file_path=output_file,
    language="en"
)
