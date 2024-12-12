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
import json
import sys
import argparse

"""
This program takes two inputs and constructs this directory structure:

../data/audio/<title>/
    full_mono.wav
    wavs/
        sentence_<n>.wav  (for each sentence)
    metadata.txt  (sorted by transcript length)
"""

def update_voice_clips_json(title, url):
    json_path = 'voice_clips.json'
    try:
        with open(json_path, 'r') as f:
            voice_clips = json.load(f)
    except FileNotFoundError:
        voice_clips = {}

    if title not in voice_clips:
        voice_clips[title] = []
    if url not in voice_clips[title]:
        voice_clips[title].append(url)

    with open(json_path, 'w') as f:
        json.dump(voice_clips, f, indent=4)

def download_youtube_audio(url, title):
    output_dir=f"../data/audio/{title}"
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


def transcribe_file(wav_file, wav_dir, existing_data):
    file_path = os.path.join(wav_dir, wav_file)
    base_name = os.path.splitext(wav_file)[0]

    # Check if the file already exists in the metadata
    if base_name in existing_data:
        return None, f"[*] Skipped (already exists): {wav_file}"

    # If not found, proceed with transcription
    transcript = transcribe_audio(file_path)
    if transcript != "Could not understand audio":
        return (base_name, transcript), f"[+] Transcribed and added: {wav_file}"
    else:
        return None, f"[!] Failed transcription for {wav_file}"


def transcribe_directory(title):
    wav_dir = f"../data/audio/{title}/wavs"
    output_file = f"../data/audio/{title}/metadata.json"

    # Get all WAV files in the directory and sort them
    wav_files = sorted([f for f in os.listdir(wav_dir) if f.endswith(".wav")])

    # Read existing data from the JSON file if it exists
    existing_data = {}
    if os.path.exists(output_file):
        with open(output_file, "r") as in_file:
            existing_data = json.load(in_file)

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for wav_file in wav_files:
            future = executor.submit(transcribe_file, wav_file, wav_dir, existing_data)
            futures.append(future)

        new_entries = {}
        for future in as_completed(futures):
            result, message = future.result()
            if result:
                base_name, transcript = result
                new_entries[base_name] = transcript
            print(message)

    # Combine existing and new entries
    all_entries = {**existing_data, **new_entries}

    # Sort entries by wav filename
    sorted_entries = dict(
        sorted(all_entries.items(), key=lambda x: int(x[0].split("_")[1]))
    )

    # Write sorted entries back to the file
    with open(output_file, "w") as out_file:
        json.dump(sorted_entries, out_file, indent=4)

    print(
        f"Finished processing. Results sorted by transcript length written to {output_file}"
    )


def main():
    parser = argparse.ArgumentParser(description="Download and process YouTube audio")
    parser.add_argument("title", help="Title for the audio clip")
    parser.add_argument("url", help="YouTube URL of the video")
    args = parser.parse_args()

    global TITLE, VIDEO_URL
    TITLE = args.title
    VIDEO_URL = args.url

    update_voice_clips_json(TITLE, VIDEO_URL)
    download_youtube_audio(VIDEO_URL, TITLE)
    break_into_sentences(TITLE)
    transcribe_directory(TITLE)


if __name__ == "__main__":
    main()
