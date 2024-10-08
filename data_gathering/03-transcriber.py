import os
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks

TITLE = "mike"

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


def main():
    # Directory containing WAV files
    wav_dir = f"../data/audio/{TITLE}/wavs"
    output_file = f"../data/audio/{TITLE}/metadata.txt"

    # Get all WAV files in the directory and sort them
    wav_files = sorted([f for f in os.listdir(wav_dir) if f.endswith(".wav")])

    # Read existing lines from the file if it exists
    existing_lines = set()
    if os.path.exists(output_file):
        with open(output_file, "r") as in_file:
            existing_lines = set(in_file.readlines())

    for i, wav_file in enumerate(wav_files):
        with open(output_file, "a") as out_file:
            # if i >= 4:
            #     break
            file_path = os.path.join(wav_dir, wav_file)
            transcript = transcribe_audio(file_path)
            if transcript != "Could not understand audio":
                new_line = f"{wav_file}|{transcript}|{transcript}\n"
                if new_line not in existing_lines:
                    out_file.write(new_line)
                    print(f"[+] Transcribed and added: {wav_file}")
                else:
                    print(f"[*] Skipped (already exists): {wav_file}")
            else:
                print(f"[!] Failed transcription for {wav_file}")

if __name__ == "__main__":
    main()