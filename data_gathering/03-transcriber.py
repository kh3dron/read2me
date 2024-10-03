import os
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks

def transcribe_audio(file_path):
    # Convert MP3 to WAV
    audio = AudioSegment.from_mp3(file_path)
    wav_path = file_path.replace('.mp3', '.wav')
    audio.export(wav_path, format="wav")

    # Initialize recognizer
    r = sr.Recognizer()

    # Transcribe audio
    with sr.AudioFile(wav_path) as source:
        audio = r.record(source)

    try:
        # Attempt transcription
        transcript = r.recognize_google(audio)
    except sr.UnknownValueError:
        transcript = "Could not understand audio"
    except sr.RequestError as e:
        transcript = f"Could not request results; {e}"

    # Remove temporary WAV file
    os.remove(wav_path)

    return transcript

def main():
    # Directory containing MP3 files
    mp3_dir = '../data/audio/splitmike'
    
    # Output file
    output_file = 'transcriptions.txt'

    # Get all MP3 files in the directory and sort them
    mp3_files = sorted([f for f in os.listdir(mp3_dir) if f.endswith('.mp3')])

    with open(output_file, 'w') as out_file:
        for mp3_file in mp3_files:
            file_path = os.path.join(mp3_dir, mp3_file)
            transcript = transcribe_audio(file_path)
            out_file.write(f"{mp3_file}: {transcript}\n\n")
            print(f"Transcribed: {mp3_file}")

if __name__ == "__main__":
    main()