# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Read2Me is a simplified Text-to-Speech (TTS) system for audiobook generation. The system has been redesigned as a modular toolkit supporting:

- CLI interface for direct audiobook generation
- Python library for programmatic integration
- REST API for web application integration (Bookshelf)
- Voice cloning from audio samples
- Automatic book chapter splitting and processing

## Architecture

The application follows a modular architecture with three main components:

### Core Components

- **CLI Tool** (`read2me_cli.py`): Command-line interface for standalone usage
- **Core Library** (`read2me_lib.py`): Python library with AudiobookGenerator class
- **Web Integration** (`bookshelf_integration.py`): Flask API for web app integration
- **Coqui TTS** (`TTS/`): Third-party TTS library with models and utilities

### Legacy Components (deprecated)

- **Flask API Server** (`app.py`): Original web server with authentication
- **Celery Worker** (`celery_worker.py`): Original async processing system
- **TTS Processing** (`endpoints/`): Original standalone scripts

### Data Structure

```
data/
├── audio/              # Voice training data organized by speaker
│   └── {speaker}/
│       ├── metadata.json
│       └── wavs/
├── split_books/        # Book content split into chapters
├── generations/        # Generated audio outputs
├── models/            # Custom trained models
└── metadata/          # Built-in model metadata
```

## Development Commands

### Quick Start

```bash
# Install simplified dependencies
pip install -r requirements_simple.txt

# Make CLI executable
chmod +x read2me_cli.py

# Test CLI
python read2me_cli.py list-voices
```

### Installation Options

```bash
# Install as package (recommended)
pip install -e .

# Use CLI from anywhere
read2me book my_book.txt --voice "Ana Florence"
```

### Legacy Services (if needed)

```bash
# Start original Flask/Celery system
./start-celery.sh
python app.py
```

### Dependencies

Simplified dependencies in `requirements_simple.txt`:

- Core: torch, torchaudio, TTS, soundfile, librosa
- Full TTS library still available in `TTS/requirements.txt`

## Usage Patterns

### CLI Interface

```bash
# Generate single audio
read2me tts "Hello world" --voice "Ana Florence"

# Create audiobook from file
read2me book my_book.txt --voice "Ana Florence" --output-dir audiobooks/

# Voice cloning
read2me book my_book.txt --voice-file sample.wav
```

### Library Usage

```python
from read2me_lib import AudiobookGenerator

generator = AudiobookGenerator()
metadata = generator.create_audiobook_from_file(
    file_path="book.txt",
    voice="Ana Florence"
)
```

### Web API Integration (for Bookshelf)

```python
from bookshelf_integration import create_app

app = create_app(output_dir="audiobooks")
app.run(host="0.0.0.0", port=5000)
```

### Bookshelf Connector

```python
from bookshelf_integration import BookshelfConnector

connector = BookshelfConnector("http://localhost:5000")
job_id = connector.generate_audiobook(text, title, voice)
status = connector.check_status(job_id)
```

## TTS Models

The system uses Coqui TTS models:

- **Default Model**: `tts_models/multilingual/multi-dataset/xtts_v2`
- **Built-in Voices**: Stored in `voice_samples/` with speaker names
- **Voice Cloning**: Uses XTTS v2 model with speaker adaptation

## File Organization

### Processing Scripts (`endpoints/`)

- `tts.py` - Generic TTS generation with built-in voices
- `clone-voice.py` - Voice cloning from audio samples
- `epub-to-chapters.py` - Book processing utilities

### Configuration

- `generation_log.json` - Tracks all TTS generations
- `docker-compose.yaml` - PostgreSQL database setup
- Service files for production deployment

## Data Management

### Voice Data Format

Audio training data follows specific structure:

- Organized by speaker name in `data/audio/`
- `metadata.json` contains transcription mappings
- WAV files in `wavs/` subdirectory

### Generation Tracking

All TTS generations logged to `generation_log.json` with:

- Task ID, voice used, input/output files
- Enables retrieval and audit capabilities

## Infrastructure

### Database

PostgreSQL database for user management and generation tracking (see `schema_notes.md` for detailed schema).

### Message Queue

Redis broker for Celery task queue management.

### GPU Support

TTS processing automatically detects and uses CUDA when available for faster inference.
