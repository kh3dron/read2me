# CLI Module

Command-line interface for Read2Me audiobook generation.

## Files

- **`read2me_cli.py`**: Main CLI script with argument parsing and command execution

## Features

### Commands
- `list-voices`: Display available built-in voices
- `tts <text>`: Generate single audio file from text
- `book <file>`: Convert text file to complete audiobook

### Options
- `--voice <name>`: Use specific built-in voice
- `--voice-file <path>`: Clone voice from audio sample
- `--output <path>`: Custom output file/directory
- `--language <code>`: Language for synthesis (default: en)

## Usage Examples

```bash
# List available voices
python read2me_cli.py list-voices

# Generate single TTS
python read2me_cli.py tts "Hello world" --voice "Ana Florence"

# Create audiobook with voice cloning
python read2me_cli.py book my_book.txt --voice-file sample.wav

# Custom output directory
python read2me_cli.py book novel.txt --output-dir audiobooks/novel/
```

## Architecture

### Class: `Read2MeCLI`
Main class handling CLI operations.

**Key Methods:**
- `list_voices()`: Display available voices from voice_samples/
- `generate_tts()`: Single audio generation with various options
- `process_book()`: Full book processing with chapter splitting
- `_split_into_chapters()`: Intelligent text chunking

**Dependencies:**
- `TTS.api`: Coqui TTS for audio generation
- `torch`: GPU/CPU device detection
- `argparse`: Command-line argument parsing

## Integration Notes

For **AI/Model Integration:**
- CLI class can be imported and used programmatically
- All methods return file paths for generated audio
- Progress feedback through print statements (no callbacks)
- Error handling with exceptions and return codes

For **Development:**
- Entry point function is `main()` for direct execution
- Modular design allows easy extension of commands
- Voice sample detection from `voice_samples/` directory
- Output directory creation and management built-in