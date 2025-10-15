import os
from pydub import AudioSegment
import torch
from TTS.api import TTS
import sys
import json

if len(sys.argv) < 3:
    print("Usage: python clone-api.py <source_clip> <input_text>")
    sys.exit(1)

input_filename = sys.argv[1]
task_id = sys.argv[2]
output_file = f"{task_id}.wav"

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"
model = "tts_models/multilingual/multi-dataset/xtts_v2"
tts = TTS(model).to(device)

with open(input_filename, "r", encoding="utf-8") as file:
    input_text = file.read()

tts.tts_to_file(
    text=input_text,
    file_path="output/" + output_file,
    speaker="Ana Florence",
    language="en",
    split_sentences=True,
)

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_file = os.path.join(base_dir, "generation_log.json")

try:
    with open(log_file, "r") as f:
        log_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    log_data = {}

log_data[task_id] = {
    "voice": "Ana Florence",
    "source_file": None,
    "input_file": input_filename,
    "output_file": output_file,
}

with open(log_file, "w") as f:
    json.dump(log_data, f, indent=4)
