import yt_dlp
import os
import subprocess
import os
import numpy as np
from pydub import AudioSegment

import os
import speech_recognition as sr
from concurrent.futures import ThreadPoolExecutor, as_completed
from pydub.silence import split_on_silence

"""
This program takes two inputs and constructs this directory structure:

../data/audio/<title>/
    full_mono.wav
    wavs/
        sentence_<n>.wav  (for each sentence)
    metadata.txt  (sorted by transcript length)
"""

TITLE = "john_stewart"
VIDEO_URL = "https://www.youtube.com/watch?v=HX-5jmQplIo"

TITLE = "mike2"
VIDEO_URL = "https://www.youtube.com/watch?v=c8CXe7PvEXo"

def download_youtube_audio(url, output_dir=f"../data/audio/{TITLE}"):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Configure yt-dlp options
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "outtmpl": os.path.join(output_dir, f"full_stereo.%(ext)s"),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Convert stereo to mono
    stereo_file = os.path.join(output_dir, "full_stereo.wav")
    mono_file = os.path.join(output_dir, "full_mono.wav")
    subprocess.run(["ffmpeg", "-i", stereo_file, "-ac", "1", mono_file])

    # Remove the stereo file
    os.remove(stereo_file)


def break_into_sentences(title):

    audio_path = f"../data/audio/{title}/full_mono.wav"
    audio = AudioSegment.from_wav(audio_path)

    min_silence_len = 500  # minimum length of silence (in ms)
    silence_thresh = -40  # silence threshold (in dB)
    keep_silence = (
        300  # amount of silence to keep at the beginning and end of each chunk (in ms)
    )

    chunks = split_on_silence(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh,
        keep_silence=keep_silence,
    )

    output_dir = f"../data/audio/{title}/wavs"
    os.makedirs(output_dir, exist_ok=True)

    # Export each chunk as a separate audio file
    for i, chunk in enumerate(chunks):
        output_path = os.path.join(output_dir, f"sentence_{i+1:05d}.wav")
        chunk.export(output_path, format="wav")

    print(f"Audio split into {len(chunks)} sentences and saved in {output_dir}")


def transcribe_audio(file_path):
    # Initialize recognizer
    r = sr.Recognizer()

    # Transcribe audio
    with sr.AudioFile(file_path) as source:
        audio = r.record(source)

    try:
        # Attempt transcription
        transcript = r.recognize_google(audio)
    except sr.UnknownValueError:
        transcript = "Could not understand audio"
    except sr.RequestError as e:
        transcript = f"Could not request results; {e}"

    return transcript


def transcribe_file(wav_file, wav_dir, existing_lines):
    file_path = os.path.join(wav_dir, wav_file)
    base_name = os.path.splitext(wav_file)[0]
    new_line = f"{base_name}|"

    # Check if the file already exists in the metadata
    for line in existing_lines:
        if line.startswith(f"{base_name}|"):
            return None, f"[*] Skipped (already exists): {wav_file}"

    # If not found, proceed with transcription
    # TODO store failures to transcribe in the same way
    transcript = transcribe_audio(file_path)
    if transcript != "Could not understand audio":
        new_line += f"{transcript}|{transcript}\n"
        return new_line, f"[+] Transcribed and added: {wav_file}"
    else:
        return None, f"[!] Failed transcription for {wav_file}"


def transcribe_directory(title):
    wav_dir = f"../data/audio/{title}/wavs"
    output_file = f"../data/audio/{title}/metadata.txt"

    # Get all WAV files in the directory and sort them
    wav_files = sorted([f for f in os.listdir(wav_dir) if f.endswith(".wav")])

    # Read existing lines from the file if it exists
    existing_lines = set()
    if os.path.exists(output_file):
        with open(output_file, "r") as in_file:
            existing_lines = set(in_file.readlines())

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for wav_file in wav_files:
            future = executor.submit(transcribe_file, wav_file, wav_dir, existing_lines)
            futures.append(future)

        new_lines = []
        for future in as_completed(futures):
            result, message = future.result()
            if result:
                new_lines.append(result)
            print(message)

    # Read all existing lines and add new lines
    all_lines = list(existing_lines) + new_lines

    # Sort all lines by transcript length
    sorted_lines = sorted(all_lines, key=lambda x: len(x.split("|")[1]))

    # Write sorted lines back to the file
    with open(output_file, "w") as out_file:
        out_file.writelines(sorted_lines)

    print(
        f"Finished processing. Results sorted by transcript length written to {output_file}"
    )


def main():
    download_youtube_audio(VIDEO_URL)
    break_into_sentences(TITLE)
    transcribe_directory(TITLE)


if __name__ == "__main__":
    main()
