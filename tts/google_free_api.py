import os
from gtts import gTTS
from pydub import AudioSegment

def text_to_speech(input_dir, output_dir, language='en'):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Get all text files in the input directory
    text_files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
    text_files.sort(key=lambda x: int(x[2:-4]))  # Sort by chapter number

    for text_file in text_files:
        input_path = os.path.join(input_dir, text_file)
        output_path = os.path.join(output_dir, text_file.replace('.txt', '.mp3'))

        print(f"Converting {text_file} to speech...")

        # Read the text file
        with open(input_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Convert text to speech
        tts = gTTS(text=text, lang=language, slow=False)

        # Save as MP3
        tts.save(output_path)

        print(f"Created {output_path}")

    print("Conversion complete!")

# Example usage
title = 'neuromancer'
input_dir = f'chapters/{title}'
output_dir = f'audio/{title}'
text_to_speech(input_dir, output_dir)