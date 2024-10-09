import os
import speech_recognition as sr
from concurrent.futures import ThreadPoolExecutor, as_completed

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


def process_file(wav_file, wav_dir, existing_lines):
    file_path = os.path.join(wav_dir, wav_file)
    transcript = transcribe_audio(file_path)
    if transcript != "Could not understand audio":
        new_line = f"{os.path.splitext(wav_file)[0]}|{transcript}|{transcript}\n"
        if new_line not in existing_lines:
            return new_line, f"[+] Transcribed and added: {wav_file}"
        else:
            return None, f"[*] Skipped (already exists): {wav_file}"
    else:
        return None, f"[!] Failed transcription for {wav_file}"

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

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for wav_file in wav_files:
            future = executor.submit(process_file, wav_file, wav_dir, existing_lines)
            futures.append(future)

        new_lines = []
        for future in as_completed(futures):
            result, message = future.result()
            if result:
                new_lines.append(result)
            print(message)

    # Read all existing lines and add new lines
    all_lines = list(existing_lines) + new_lines

    # Sort all lines
    sorted_lines = sorted(all_lines)

    # Write sorted lines back to the file
    with open(output_file, "w") as out_file:
        out_file.writelines(sorted_lines)

    print(f"Finished processing. Sorted results written to {output_file}")

if __name__ == "__main__":
    main()