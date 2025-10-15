# Library Module

Core library for Read2Me audiobook generation. Designed for programmatic integration.

## Files

- **`read2me_lib.py`**: Main library with AudiobookGenerator class and convenience functions

## Core Classes

### `AudiobookGenerator`
Main class for all TTS operations.

**Initialization:**
```python
generator = AudiobookGenerator(
    output_dir="output",  # Default output directory
    model="tts_models/multilingual/multi-dataset/xtts_v2"  # TTS model
)
```

**Key Methods:**

#### `generate_audio(text, voice=None, voice_file=None, language="en", output_filename=None, progress_callback=None)`
Generate single audio file from text.

**Parameters:**
- `text` (str): Text to synthesize
- `voice` (str, optional): Built-in voice name
- `voice_file` (str, optional): Path to voice sample for cloning
- `language` (str): Language code (default: "en")
- `output_filename` (str, optional): Custom output filename
- `progress_callback` (callable, optional): Function for progress updates

**Returns:** `str` - Path to generated audio file

#### `create_audiobook(text, title, voice=None, voice_file=None, language="en", max_chapter_length=10000, progress_callback=None)`
Create complete audiobook from text.

**Parameters:**
- `text` (str): Full book text
- `title` (str): Book title for output directory
- `voice` (str, optional): Built-in voice name
- `voice_file` (str, optional): Path to voice sample for cloning
- `language` (str): Language code
- `max_chapter_length` (int): Maximum characters per chapter
- `progress_callback` (callable, optional): Progress update function

**Returns:** `dict` - Metadata with audiobook information

#### `create_audiobook_from_file(file_path, voice=None, voice_file=None, language="en", progress_callback=None)`
Create audiobook from text file.

**Parameters:**
- `file_path` (str): Path to input text file
- Other parameters same as `create_audiobook`

**Returns:** `dict` - Audiobook metadata

#### `get_available_voices()`
Get list of available built-in voices.

**Returns:** `list` - Sorted list of voice names

## Convenience Functions

### `quick_tts(text, voice=None, output_file=None)`
Quick TTS generation without class instantiation.

### `book_to_audio(file_path, voice=None, progress_callback=None)`
Quick audiobook conversion from file.

## Usage Examples

### Basic Usage
```python
from read2me_lib import AudiobookGenerator

# Initialize
generator = AudiobookGenerator()

# Simple audio generation
audio_path = generator.generate_audio(
    text="Hello, this is a test",
    voice="Ana Florence"
)

# Get available voices
voices = generator.get_available_voices()
print(f"Available voices: {voices}")
```

### Audiobook Creation
```python
# Create audiobook from text
metadata = generator.create_audiobook(
    text=long_text,
    title="My Novel",
    voice="Ana Florence",
    max_chapter_length=8000
)

print(f"Created {metadata['total_chapters']} chapters")
print(f"Output directory: {metadata['output_directory']}")
```

### With Progress Tracking
```python
def my_progress_callback(message):
    print(f"[PROGRESS] {message}")

# Create audiobook with progress updates
metadata = generator.create_audiobook_from_file(
    file_path="book.txt",
    voice="Ana Florence",
    progress_callback=my_progress_callback
)
```

### Voice Cloning
```python
# Clone voice from sample
audio_path = generator.generate_audio(
    text="Hello in cloned voice",
    voice_file="path/to/voice_sample.wav"
)
```

## Architecture Notes

### Text Processing
- **Chapter Splitting**: Automatic text division at paragraph boundaries
- **Length Management**: Configurable maximum chapter length
- **Encoding**: UTF-8 file reading with error handling

### Audio Generation
- **Lazy Loading**: TTS model loaded only when needed
- **Device Detection**: Automatic GPU/CPU selection
- **Output Management**: Organized directory structure with metadata

### Error Handling
- File not found exceptions for input files
- TTS generation error catching and re-raising
- Empty text validation

## Integration Guidelines

### For AI/Model Development:
1. **Callback System**: Use `progress_callback` for real-time updates
2. **Metadata Structure**: Consistent JSON output with file paths and chapter info
3. **Device Management**: Automatic CUDA detection and fallback
4. **Memory Management**: Chapter-based processing prevents memory issues

### For Web Applications:
1. **Async Compatibility**: Can be wrapped in threading or async frameworks
2. **File Path Returns**: All methods return absolute paths for easy file serving
3. **Progress Tracking**: Callback system enables real-time UI updates
4. **Error Propagation**: Exceptions bubble up for proper error handling

### Output Structure:
```
output/
└── Book_Title/
    ├── metadata.json      # Complete audiobook metadata
    ├── chapter_01.wav     # Chapter audio files
    ├── chapter_02.wav
    └── ...
```

### Metadata Format:
```json
{
  "title": "Book Title",
  "total_chapters": 5,
  "voice_used": "Ana Florence",
  "language": "en",
  "output_directory": "/path/to/output/Book_Title",
  "audio_files": [
    {
      "chapter": 1,
      "filename": "chapter_01.wav",
      "path": "/full/path/to/chapter_01.wav",
      "duration": null
    }
  ],
  "created_at": "timestamp"
}
```