import os
import numpy as np
from pydub import AudioSegment
from pydub.silence import split_on_silence

# Load the audio file
TITLE = "mike"
audio_path = f"../data/audio/{TITLE}/full.wav"
audio = AudioSegment.from_wav(audio_path)

# Define parameters for splitting
min_silence_len = 500  # minimum length of silence (in ms)
silence_thresh = -40  # silence threshold (in dB)
keep_silence = 300  # amount of silence to keep at the beginning and end of each chunk (in ms)

# Split the audio into chunks based on silence
chunks = split_on_silence(
    audio,
    min_silence_len=min_silence_len,
    silence_thresh=silence_thresh,
    keep_silence=keep_silence
)

# Create the output directory if it doesn't exist
output_dir = f"../data/audio/{TITLE}/wavs"
os.makedirs(output_dir, exist_ok=True)

# Export each chunk as a separate audio file
for i, chunk in enumerate(chunks):
    output_path = os.path.join(output_dir, f"sentence_{i+1:05d}.wav")
    chunk.export(output_path, format="wav")

print(f"Audio split into {len(chunks)} sentences and saved in {output_dir}")
