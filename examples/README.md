# Examples

This directory contains example scripts and usage patterns for Read2Me.

## Planned Examples

### Basic Usage Examples
- **Simple TTS**: Basic text-to-speech generation
- **Voice Cloning**: Using custom voice samples
- **Book Processing**: Converting text files to audiobooks

### Integration Examples
- **Flask Integration**: Embedding Read2Me in Flask applications
- **Django Integration**: Using Read2Me with Django projects
- **Async Processing**: Asynchronous audiobook generation
- **Progress Tracking**: Real-time progress updates

### Advanced Examples
- **Custom Voice Training**: Training custom TTS voices
- **Batch Processing**: Processing multiple books
- **API Client**: Complete API client implementation
- **Web Interface**: Simple web UI for audiobook generation

## Quick Examples

### CLI Usage
```bash
# Generate single audio file
read2me tts "Hello, this is a test of the text-to-speech system."

# Create audiobook from text file
read2me book sample_book.txt --voice "Ana Florence"

# List available voices
read2me list-voices
```

### Library Usage
```python
from read2me import AudiobookGenerator

# Initialize generator
generator = AudiobookGenerator()

# Create audiobook
metadata = generator.create_audiobook(
    text="Your book content here...",
    title="My First Audiobook",
    voice="Ana Florence"
)

print(f"Audiobook created: {metadata['output_directory']}")
```

### API Usage
```python
from read2me import BookshelfConnector

# Connect to API
connector = BookshelfConnector("http://localhost:5000")

# Start generation
job_id = connector.generate_audiobook(
    book_text="Long book content...",
    book_title="My Novel",
    voice="Viktor Eka"
)

# Check status
status = connector.check_status(job_id)
print(f"Status: {status['status']}")
```

## File Structure

When examples are added, they will be organized as:

```
examples/
├── basic/
│   ├── simple_tts.py
│   ├── voice_cloning.py
│   └── book_conversion.py
├── integration/
│   ├── flask_example.py
│   ├── django_example.py
│   └── async_example.py
├── advanced/
│   ├── batch_processing.py
│   ├── custom_voices.py
│   └── web_interface/
├── data/
│   ├── sample_book.txt
│   └── voice_samples/
└── README.md
```

## Contributing Examples

To add new examples:

1. Create appropriate subdirectory (`basic/`, `integration/`, `advanced/`)
2. Include complete, runnable code
3. Add comments explaining each step
4. Include sample data if needed
5. Update this README with description

### Example Template
```python
"""
Example: [Title]
Description: [What this example demonstrates]
Requirements: [Any additional dependencies]
"""

# Imports
from read2me import AudiobookGenerator

def main():
    """Main example function"""
    # Example code here
    pass

if __name__ == "__main__":
    main()
```

## Running Examples

### Prerequisites
```bash
# Install Read2Me
pip install -e .

# Or install dependencies
pip install -r config/requirements_simple.txt
```

### Sample Data
Examples will include sample text files and voice samples for testing.

### Expected Output
Each example will document expected output format and file locations.

## Use Cases Covered

1. **Simple TTS**: Converting short text to speech
2. **Book Conversion**: Full book audiobook generation
3. **Voice Customization**: Using different voices and cloning
4. **Web Integration**: Adding audiobook generation to web apps
5. **Batch Operations**: Processing multiple files efficiently
6. **Real-time Updates**: Progress tracking and status monitoring
7. **Error Handling**: Robust error management patterns
8. **Performance Optimization**: Efficient processing techniques

## Documentation Links

- **Usage Guide**: `../docs/USAGE.md`
- **API Documentation**: `../src/read2me/api/README.md`
- **Library Documentation**: `../src/read2me/lib/README.md`
- **CLI Documentation**: `../src/read2me/cli/README.md`