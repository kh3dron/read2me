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

book_name = "the_last_question"
note = "xtts_v2"

speaker = "steve_jobs"
source = "../data/audio/steve_jobs/full_mono.wav"

text_dir = f"../data/split_books/{book_name}"
output_dir = f"../output_audio/{book_name}-{note}"
os.makedirs(output_dir, exist_ok=True)

audio_segments = []
for filename in sorted(os.listdir(text_dir)):
    if filename.endswith(".txt"):
        text_path = os.path.join(text_dir, filename)

        with open(text_path, "r", encoding="utf-8") as file:
            text_content = file.read()

        audio_filename = f"{os.path.splitext(filename)[0]}.wav"
        audio_path = os.path.join(output_dir, audio_filename)

        tts.tts_to_file(
            text=text_content,
            speaker_wav=source,
            voice_dir=source,
            # speaker=speaker,
            file_path=audio_path,
            language="en"
        )

        audio_segments.append(AudioSegment.from_wav(audio_path))

combined_audio = sum(audio_segments)
audiobook_path = os.path.join(output_dir, f"{book_name}-{note}.wav")
combined_audio.export(audiobook_path, format="wav")

print(f"Audiobook generated: {audiobook_path}")
# os.rename(audiobook_path, f"/media/tristan/Seagate7/media/audiobooks/{book_name}-{note}.wav")
