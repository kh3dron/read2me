# Source Code

This directory contains the main Read2Me source code organized into three modules:

## Structure

```
src/
└── read2me/
    ├── cli/          # Command-line interface
    ├── lib/          # Core library
    ├── api/          # Web API integration
    └── __init__.py   # Package initialization
```

## Modules

### CLI (`cli/`)
Command-line interface for standalone audiobook generation.
- **Entry point**: `read2me_cli.py`
- **Purpose**: Direct command-line usage
- **Key features**: Voice listing, single TTS, book processing

### Library (`lib/`)
Core library with the main AudiobookGenerator class.
- **Entry point**: `read2me_lib.py`
- **Purpose**: Programmatic integration
- **Key features**: AudiobookGenerator class, convenience functions

### API (`api/`)
Web API for integration with web applications like Bookshelf.
- **Entry point**: `bookshelf_integration.py`
- **Purpose**: REST API and connector classes
- **Key features**: Flask app, job management, BookshelfConnector

## Installation

```bash
# Install as package
pip install -e .

# Import in Python
from read2me import AudiobookGenerator, quick_tts, BookshelfConnector
```

## Usage

See individual README files in each subdirectory for detailed usage instructions.