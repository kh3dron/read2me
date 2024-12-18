import os
from pydub import AudioSegment
import torch
from TTS.api import TTS
import sys
import json

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
output_file = f"{task_id}.wav"

tts.tts_to_file(
    text=input_text,
    speaker_wav=source_clip,
    file_path="output/" + output_file,
    language="en"
)

# Get the absolute path to generation_log.json
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_file = os.path.join(base_dir, "generation_log.json")

# Update the JSON log with proper formatting
try:
    # Read existing data
    with open(log_file, "r") as f:
        log_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    log_data = {}

# Create new entry
log_data[task_id] = {
    "voice": os.path.basename(os.path.dirname(os.path.dirname(source_clip))),
    "source_file": source_clip,
    "input_text": input_text,
    "output_file": output_file
}

# Write updated data
with open(log_file, "w") as f:
    json.dump(log_data, f, indent=4)

