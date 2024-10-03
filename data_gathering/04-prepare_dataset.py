import os
import json

def prepare_dataset(audio_dir, transcript_file, output_file):
    dataset = []
    
    with open(transcript_file, 'r') as f:
        transcripts = f.readlines()
    
    for line in transcripts:
        if line.strip():
            filename, text = line.strip().split(':', 1)
            audio_path = os.path.join(audio_dir, filename.strip())
            if text.strip() != "Could not understand audio":
                if os.path.exists(audio_path):
                    dataset.append({
                        "audio_file": audio_path,
                        "text": text.strip()
                })
    
    with open(output_file, 'w') as f:
        json.dump(dataset, f, indent=2)

    print(f"Dataset prepared and saved to {output_file}")

if __name__ == "__main__":
    audio_dir = '../data/audio/splitmike'
    transcript_file = 'transcriptions.txt'
    output_file = 'tts_dataset.json'
    prepare_dataset(audio_dir, transcript_file, output_file)
