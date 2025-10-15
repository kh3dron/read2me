# Read2Me Usage Guide

## Overview

Read2Me has been simplified into a modular system with three main components:

1. **CLI Tool** (`read2me_cli.py`) - Command-line interface for direct usage
2. **Library** (`read2me_lib.py`) - Python library for programmatic integration
3. **Web API** (`bookshelf_integration.py`) - REST API for web application integration

## Installation

### Quick Setup

```bash
# Install dependencies
pip install -r requirements_simple.txt

# Make CLI executable
chmod +x read2me_cli.py
```

### Full Installation

```bash
# Install as package
pip install -e .

# Now you can use 'read2me' command anywhere
read2me --help
```

## CLI Usage

### List Available Voices

```bash
python read2me_cli.py list-voices
```

### Generate Single Audio

```bash
# Using default voice
python read2me_cli.py tts "Hello, this is a test."

# Using specific voice
python read2me_cli.py tts "Hello world" --voice "Ana Florence"

# Voice cloning
python read2me_cli.py tts "Hello world" --voice-file path/to/sample.wav

# Custom output file
python read2me_cli.py tts "Hello world" --output my_audio.wav
```

### Generate Audiobook from File

```bash
# Basic audiobook generation
python read2me_cli.py book my_book.txt

# With specific voice
python read2me_cli.py book my_book.txt --voice "Ana Florence"

# Voice cloning
python read2me_cli.py book my_book.txt --voice-file voice_sample.wav

# Custom output directory
python read2me_cli.py book my_book.txt --output-dir my_audiobook/
```

## Library Usage

### Basic Audio Generation

```python
from read2me_lib import AudiobookGenerator

# Initialize generator
generator = AudiobookGenerator()

# Generate simple audio
audio_path = generator.generate_audio(
    text="Hello, this is a test",
    voice="Ana Florence"
)
print(f"Audio saved to: {audio_path}")
```

### Create Audiobook

```python
# From text
metadata = generator.create_audiobook(
    text=long_text,
    title="My Book",
    voice="Ana Florence"
)

# From file
metadata = generator.create_audiobook_from_file(
    file_path="book.txt",
    voice="Ana Florence"
)

print(f"Audiobook created in: {metadata['output_directory']}")
print(f"Total chapters: {metadata['total_chapters']}")
```

### With Progress Tracking

```python
def progress_callback(message):
    print(f"Progress: {message}")

metadata = generator.create_audiobook_from_file(
    file_path="book.txt",
    progress_callback=progress_callback
)
```

### Quick Functions

```python
from read2me_lib import quick_tts, book_to_audio

# Quick TTS
audio_file = quick_tts("Hello world", voice="Ana Florence")

# Quick book conversion
book_metadata = book_to_audio("my_book.txt")
```

## Web API Integration

### Start the API Server

```python
from bookshelf_integration import create_app

app = create_app(output_dir="audiobooks")
app.run(host="0.0.0.0", port=5000)
```

### API Endpoints

#### Health Check

```bash
curl http://localhost:5000/health
```

#### List Voices

```bash
curl http://localhost:5000/voices
```

#### Generate Audiobook

```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your book text here",
    "title": "My Book",
    "voice": "Ana Florence"
  }'
```

#### Check Status

```bash
curl http://localhost:5000/status/JOB_ID
```

#### Download Results

```bash
# Download metadata
curl http://localhost:5000/download/JOB_ID

# Download specific chapter
curl http://localhost:5000/download/JOB_ID/chapter/1
```

## Bookshelf Integration

### Using the Connector Class

```python
from bookshelf_integration import BookshelfConnector

# Initialize connector
connector = BookshelfConnector("http://localhost:5000")

# Generate audiobook
job_id = connector.generate_audiobook(
    book_text="Your book content here",
    book_title="My Book",
    voice="Ana Florence"
)

# Check status
status = connector.check_status(job_id)
print(f"Status: {status['status']}, Progress: {status['progress']}")

# Get available voices
voices = connector.get_available_voices()
print(f"Available voices: {voices}")
```

### Example Web App Integration

```python
from flask import Flask, render_template, request, jsonify
from bookshelf_integration import BookshelfConnector

app = Flask(__name__)
audio_connector = BookshelfConnector()

@app.route('/create_audiobook', methods=['POST'])
def create_audiobook():
    book_id = request.json['book_id']
    voice = request.json.get('voice', 'Ana Florence')
    
    # Get book content from your database
    book_content = get_book_content(book_id)  # Your function
    book_title = get_book_title(book_id)      # Your function
    
    # Start audiobook generation
    job_id = audio_connector.generate_audiobook(book_content, book_title, voice)
    
    # Store job_id with book_id in your database
    store_audiobook_job(book_id, job_id)  # Your function
    
    return jsonify({"job_id": job_id, "status": "started"})

@app.route('/audiobook_status/<book_id>')
def audiobook_status(book_id):
    job_id = get_audiobook_job_id(book_id)  # Your function
    if job_id:
        status = audio_connector.check_status(job_id)
        return jsonify(status)
    return jsonify({"error": "No audiobook job found"})
```

## Configuration

### Voice Samples

Place voice sample files in `voice_samples/` directory:

```
voice_samples/
├── Ana Florence.wav
├── Viktor Eka.wav
└── Custom Voice.wav
```

### Output Structure

Generated audiobooks follow this structure:

```
output/
└── My_Book/
    ├── metadata.json
    ├── chapter_01.wav
    ├── chapter_02.wav
    └── ...
```

### Environment Variables

```bash
# Optional: Set custom model
export TTS_MODEL="tts_models/multilingual/multi-dataset/xtts_v2"

# Optional: Set output directory
export AUDIOBOOK_OUTPUT_DIR="./audiobooks"
```

## Performance Tips

1. **GPU Acceleration**: Ensure CUDA is available for faster generation
2. **Chapter Length**: Adjust `max_chapter_length` based on memory constraints
3. **Voice Samples**: Use high-quality voice samples (16kHz+) for better cloning
4. **Batch Processing**: Process multiple books sequentially to avoid memory issues

## Troubleshooting

### Common Issues

1. **Out of Memory**: Reduce chapter length or use CPU instead of GPU
2. **Voice Not Found**: Check `voice_samples/` directory and file names
3. **Model Loading Errors**: Ensure all dependencies are installed correctly

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Your code here
```
