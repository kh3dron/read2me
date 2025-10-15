# Read2Me

Simple, modular toolkit for generating audiobooks from text using AI-powered text-to-speech.

## Quick Start

```bash
# Install dependencies
pip install -r config/requirements_simple.txt

# Generate audiobook from text file
python src/read2me/cli/read2me_cli.py book my_book.txt --voice "Ana Florence"

# Or install as package
pip install -e .
read2me book my_book.txt --voice "Ana Florence"
```

## Overview

Read2Me is a streamlined audiobook generation system with three main components:

1. **CLI Tool** - Command-line interface for direct usage
2. **Python Library** - For programmatic integration
3. **Web API** - REST API for web application integration (Bookshelf)

## Features

- **Multiple Voices**: Built-in voices and voice cloning support
- **Automatic Chapters**: Intelligent text splitting for long books
- **Progress Tracking**: Real-time generation progress
- **Multiple Formats**: Support for various text input formats
- **Web Integration**: Easy integration with web applications
- **GPU Acceleration**: CUDA support for faster generation

## Repository Structure

```
read2me/
├── src/                    # Main source code
│   └── read2me/
│       ├── cli/           # Command-line interface
│       ├── lib/           # Core library
│       └── api/           # Web API integration
├── docs/                  # Documentation
│   ├── USAGE.md          # Comprehensive usage guide
│   └── research/         # Technical research notes
├── config/               # Configuration and setup
│   ├── requirements_simple.txt
│   └── setup.py
├── examples/             # Usage examples (planned)
├── legacy/               # Original Flask/Celery implementation
├── voice_samples/        # Built-in voice samples
├── data/                 # Data directories
└── CLAUDE.md            # AI development guidance
```

## Installation

### Method 1: Direct Installation
```bash
# Install dependencies
pip install -r config/requirements_simple.txt

# Make CLI executable
chmod +x src/read2me/cli/read2me_cli.py
```

### Method 2: Package Installation (Recommended)
```bash
# Install as package
pip install -e .

# Use from anywhere
read2me --help
```

## Usage

### Command Line Interface
```bash
# List available voices
read2me list-voices

# Generate single audio
read2me tts "Hello, world!" --voice "Ana Florence"

# Create audiobook from file
read2me book my_novel.txt --voice "Viktor Eka"

# Voice cloning
read2me book my_book.txt --voice-file custom_voice.wav
```

### Python Library
```python
from read2me import AudiobookGenerator

# Initialize generator
generator = AudiobookGenerator()

# Create audiobook
metadata = generator.create_audiobook_from_file(
    file_path="book.txt",
    voice="Ana Florence"
)

print(f"Audiobook created: {metadata['output_directory']}")
```

### Web API Integration
```python
from read2me import BookshelfConnector

# Connect to API server
connector = BookshelfConnector("http://localhost:5000")

# Generate audiobook
job_id = connector.generate_audiobook(
    book_text="Your book content...",
    book_title="My Book",
    voice="Ana Florence"
)

# Check status
status = connector.check_status(job_id)
```

## Documentation

- **[Usage Guide](docs/USAGE.md)** - Comprehensive examples and API documentation
- **[Source Documentation](src/README.md)** - Code organization and module details
- **[Configuration](config/README.md)** - Setup and configuration options
- **[Legacy System](legacy/README.md)** - Original implementation reference

## Voice Samples

Place voice samples in the `voice_samples/` directory:
```
voice_samples/
├── Ana Florence.wav
├── Viktor Eka.wav
└── Your Custom Voice.wav
```

## Requirements

- Python 3.8+
- PyTorch 2.1+
- 4GB+ RAM (8GB+ recommended)
- Optional: CUDA-compatible GPU for faster generation

## Dependencies

Core dependencies (see `config/requirements_simple.txt`):
- `torch` - Neural network framework
- `TTS` - Coqui TTS library
- `soundfile` - Audio file processing
- `librosa` - Audio analysis

## Development

### Structure Overview
- **`src/read2me/cli/`** - Command-line interface
- **`src/read2me/lib/`** - Core AudiobookGenerator library
- **`src/read2me/api/`** - Web API and Bookshelf integration
- **`legacy/`** - Original Flask/Celery implementation (deprecated)

### Contributing
1. Read the module-specific README files in `src/read2me/*/`
2. Follow the code organization patterns
3. Update documentation for any changes
4. Test with both CLI and library interfaces

## Migration from Legacy

If you're using the original Flask/Celery system:
1. Review `legacy/README.md` for migration guidance
2. Map old API endpoints to new library methods
3. Replace Celery tasks with direct library calls
4. Update authentication to application level

## Performance

- **GPU**: Automatic CUDA detection for faster generation
- **Memory**: Chapter-based processing prevents memory issues
- **Concurrency**: Multiple simultaneous generations supported in API mode

## Troubleshooting

Common issues and solutions in `docs/USAGE.md#troubleshooting`.

## License

[Add your license information here]

## Support

- Documentation: See `docs/` directory
- Issues: [GitHub Issues](your-repo-url/issues)
- Examples: See `examples/` directory (coming soon)