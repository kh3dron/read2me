# Tests

Test suite for Read2Me components.

## Structure

```
tests/
├── cli/          # CLI component tests
├── lib/          # Library component tests
├── api/          # API component tests
└── README.md     # This file
```

## Running Tests

### Prerequisites
```bash
# Install test dependencies
pip install pytest pytest-cov

# Install Read2Me in development mode
pip install -e .
```

### Test Execution
```bash
# Run all tests
pytest tests/

# Run specific component tests
pytest tests/lib/
pytest tests/cli/
pytest tests/api/

# Run with coverage
pytest --cov=src/read2me tests/
```

## Test Organization

### Library Tests (`lib/`)
- AudiobookGenerator class functionality
- Text processing and chapter splitting
- Voice management and selection
- File I/O operations
- Error handling

### CLI Tests (`cli/`)
- Command-line argument parsing
- CLI command execution
- Output file generation
- Error handling and exit codes

### API Tests (`api/`)
- Flask app endpoints
- Job management and status tracking
- BookshelfConnector functionality
- API error responses

## Test Data

Test files should be placed in appropriate subdirectories:
```
tests/
├── data/
│   ├── sample_text.txt
│   ├── short_book.txt
│   └── voice_samples/
└── fixtures/
    ├── expected_outputs/
    └── mock_responses/
```

## Writing Tests

### Test Template
```python
import pytest
from read2me import AudiobookGenerator

class TestAudiobookGenerator:
    def setup_method(self):
        """Setup for each test method"""
        self.generator = AudiobookGenerator(output_dir="test_output")
    
    def test_feature(self):
        """Test specific feature"""
        # Test implementation
        pass
    
    def teardown_method(self):
        """Cleanup after each test"""
        # Cleanup code
        pass
```

### Mock Usage
```python
from unittest.mock import patch, MagicMock

@patch('read2me.lib.read2me_lib.TTS')
def test_with_mock_tts(mock_tts):
    """Test with mocked TTS to avoid model loading"""
    mock_tts.return_value.to.return_value = MagicMock()
    # Test implementation
```

## Continuous Integration

Tests should be run on:
- Multiple Python versions (3.8, 3.9, 3.10, 3.11)
- Different operating systems (Linux, macOS, Windows)
- With and without GPU support

## Performance Tests

Include performance benchmarks for:
- Text processing speed
- Audio generation time
- Memory usage patterns
- Concurrent request handling

## Integration Tests

Test full workflows:
- End-to-end audiobook generation
- CLI to library integration
- API client to server communication
- File system operations