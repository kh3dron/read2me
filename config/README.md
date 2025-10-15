# Configuration

This directory contains configuration files and installation scripts for Read2Me.

## Files

### Dependencies
- **`requirements_simple.txt`**: Simplified dependencies for Read2Me
  - Core TTS functionality only
  - Minimal dependencies for easy installation
  - Recommended for new installations

### Installation
- **`setup.py`**: Python package setup configuration
  - Package metadata and dependencies
  - Entry point definitions for CLI
  - Installation instructions

## Installation Methods

### Method 1: Direct Dependencies
```bash
pip install -r config/requirements_simple.txt
```

### Method 2: Package Installation
```bash
pip install -e .
```

This installs Read2Me as a package and creates the `read2me` command.

## Configuration Options

### Environment Variables

#### TTS Model Configuration
```bash
# Set custom TTS model
export TTS_MODEL="tts_models/multilingual/multi-dataset/xtts_v2"

# Alternative models
export TTS_MODEL="tts_models/en/ljspeech/tacotron2-DDC"
```

#### Output Directory
```bash
# Set default output directory
export AUDIOBOOK_OUTPUT_DIR="./audiobooks"
export READ2ME_OUTPUT_DIR="/var/audiobooks"
```

#### Voice Samples
```bash
# Custom voice samples directory
export VOICE_SAMPLES_DIR="./custom_voices"
```

### File Locations

#### Voice Samples
Default location: `voice_samples/`
```
voice_samples/
├── Ana Florence.wav
├── Viktor Eka.wav
├── Gracie Wise.wav
└── Custom Voice.wav
```

#### Output Structure
Default location: `output/` or configured directory
```
output/
├── Book_Title_1/
│   ├── metadata.json
│   ├── chapter_01.wav
│   └── chapter_02.wav
└── Book_Title_2/
    └── ...
```

## Dependencies Explanation

### Core Dependencies (`requirements_simple.txt`)
```
torch>=2.1              # PyTorch for neural networks
torchaudio              # Audio processing
TTS>=0.22.0             # Coqui TTS library
soundfile>=0.12.0       # Audio file I/O
librosa>=0.10.0         # Audio analysis
numpy>=1.24.3           # Numerical computing
pyyaml>=6.0             # Configuration files
```

### Optional Dependencies
```bash
# For web API (if using bookshelf_integration.py)
pip install flask requests

# For development
pip install pytest black flake8

# For GPU acceleration (if available)
pip install torch[cuda]
```

## Setup Script Details

### Package Information
- **Name**: read2me
- **Version**: 1.0.0
- **Entry Point**: `read2me` command points to CLI

### Console Scripts
After installation, these commands become available:
```bash
read2me list-voices
read2me tts "Hello world"
read2me book my_book.txt
```

## Platform-Specific Notes

### Windows
```bash
# Use pip in Windows
pip install -r config\requirements_simple.txt

# May need Visual Studio build tools for some dependencies
```

### macOS
```bash
# May need Homebrew for audio libraries
brew install portaudio
pip install -r config/requirements_simple.txt
```

### Linux
```bash
# Install audio system dependencies
sudo apt-get install portaudio19-dev python3-dev
pip install -r config/requirements_simple.txt
```

## GPU Support

### CUDA Setup
For faster generation with GPU:
```bash
# Check CUDA availability
python -c "import torch; print(torch.cuda.is_available())"

# Install CUDA-enabled PyTorch if needed
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Memory Requirements
- **CPU**: 4GB+ RAM recommended
- **GPU**: 6GB+ VRAM for optimal performance
- **Storage**: 2GB+ for TTS models

## Troubleshooting

### Common Issues

#### Missing Audio Libraries
```bash
# Linux
sudo apt-get install libsndfile1-dev

# macOS
brew install libsndfile

# Windows
# Usually included with Python audio packages
```

#### TTS Model Download Errors
```bash
# Manually download models
python -c "from TTS.api import TTS; TTS('tts_models/multilingual/multi-dataset/xtts_v2')"
```

#### Permission Errors
```bash
# Use user installation
pip install --user -r config/requirements_simple.txt
```

## Development Setup

### Full Development Environment
```bash
# Clone repository
git clone <repository-url>
cd read2me

# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest black flake8 mypy

# Run tests
pytest tests/
```

### Docker Setup (Optional)
```dockerfile
FROM python:3.9

WORKDIR /app
COPY config/requirements_simple.txt .
RUN pip install -r requirements_simple.txt

COPY src/ ./src/
RUN pip install -e .

CMD ["read2me", "--help"]
```

## Production Deployment

### System Service
For web API deployment:
```bash
# Copy service file
sudo cp legacy/tts-api.service /etc/systemd/system/

# Modify paths in service file
sudo systemctl enable tts-api
sudo systemctl start tts-api
```

### Load Balancing
For high-volume usage:
- Use multiple API instances
- Implement job queue (Redis/RabbitMQ)
- Consider GPU cluster for processing