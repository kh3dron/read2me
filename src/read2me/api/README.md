# API Module

Web API and integration components for Read2Me. Designed for integration with web applications like Bookshelf.

## Files

- **`bookshelf_integration.py`**: Complete web API with Flask app and connector classes

## Core Classes

### `BookshelfAudioAPI`
Backend API manager handling job queues and audiobook generation.

**Initialization:**
```python
api = BookshelfAudioAPI(output_dir="audiobooks")
```

**Key Methods:**

#### `create_job(text, title, voice=None, voice_file=None, language="en")`
Create new audiobook generation job.

**Parameters:**
- `text` (str): Full book text
- `title` (str): Book title
- `voice` (str, optional): Built-in voice name
- `voice_file` (str, optional): Voice sample path for cloning
- `language` (str): Language code

**Returns:** `str` - Unique job ID

#### `create_job_from_file(file_path, voice=None, voice_file=None, language="en")`
Create job from text file.

#### `get_job_status(job_id)`
Get current job status and progress.

**Returns:** `dict` - Job status information

#### `get_job_result(job_id)`
Get completed job result path.

**Returns:** `str` - Path to output directory

#### `list_voices()`
Get available voice list.

### `BookshelfConnector`
Client connector for easy integration with web applications.

**Initialization:**
```python
connector = BookshelfConnector("http://localhost:5000")
```

**Key Methods:**

#### `generate_audiobook(book_text, book_title, voice=None)`
Start audiobook generation remotely.

**Returns:** `str` - Job ID for tracking

#### `check_status(job_id)`
Check generation status.

**Returns:** `dict` - Status information

#### `get_available_voices()`
Get list of available voices from API.

## Flask Web API

### Endpoints

#### Health Check
- **URL:** `/health`
- **Method:** GET
- **Response:** `{"status": "ok"}`

#### List Voices
- **URL:** `/voices`
- **Method:** GET
- **Response:** `{"voices": ["Ana Florence", "Viktor Eka", ...]}`

#### Generate Audiobook
- **URL:** `/generate`
- **Method:** POST
- **Body:**
  ```json
  {
    "text": "Book content here",
    "title": "Book Title",
    "voice": "Ana Florence",
    "language": "en"
  }
  ```
- **Response:**
  ```json
  {
    "job_id": "uuid-string",
    "status": "pending",
    "message": "Audiobook generation started"
  }
  ```

#### Generate from File
- **URL:** `/generate/file`
- **Method:** POST
- **Body:**
  ```json
  {
    "file_path": "/path/to/book.txt",
    "voice": "Ana Florence",
    "language": "en"
  }
  ```

#### Check Status
- **URL:** `/status/<job_id>`
- **Method:** GET
- **Response:**
  ```json
  {
    "status": "processing|completed|failed|pending",
    "progress": "Current progress message",
    "title": "Book Title",
    "voice": "Ana Florence",
    "result": {...},
    "error": "Error message if failed"
  }
  ```

#### Download Metadata
- **URL:** `/download/<job_id>`
- **Method:** GET
- **Response:** File download of metadata.json

#### Download Chapter
- **URL:** `/download/<job_id>/chapter/<chapter_num>`
- **Method:** GET
- **Response:** WAV file download

## Usage Examples

### Starting the API Server
```python
from bookshelf_integration import create_app

app = create_app(output_dir="audiobooks")
app.run(host="0.0.0.0", port=5000, debug=True)
```

### Using the Connector
```python
from bookshelf_integration import BookshelfConnector

# Initialize connector
connector = BookshelfConnector("http://localhost:5000")

# Start audiobook generation
job_id = connector.generate_audiobook(
    book_text="Long book content here...",
    book_title="My Novel",
    voice="Ana Florence"
)

# Check status
status = connector.check_status(job_id)
print(f"Status: {status['status']}")
print(f"Progress: {status['progress']}")

# Get available voices
voices = connector.get_available_voices()
```

### Direct API Usage
```python
from bookshelf_integration import BookshelfAudioAPI

# Initialize API backend
api = BookshelfAudioAPI(output_dir="audiobooks")

# Create job
job_id = api.create_job(
    text="Book content",
    title="My Book",
    voice="Ana Florence"
)

# Monitor progress
import time
while True:
    status = api.get_job_status(job_id)
    print(f"Status: {status['status']} - {status['progress']}")
    
    if status['status'] in ['completed', 'failed']:
        break
    time.sleep(5)
```

## Integration with Web Applications

### Flask App Integration
```python
from flask import Flask, request, jsonify
from bookshelf_integration import BookshelfConnector

app = Flask(__name__)
audio_connector = BookshelfConnector("http://localhost:5000")

@app.route('/books/<int:book_id>/audiobook', methods=['POST'])
def create_audiobook(book_id):
    # Get book from your database
    book = get_book_from_database(book_id)
    
    # Start audiobook generation
    job_id = audio_connector.generate_audiobook(
        book_text=book.content,
        book_title=book.title,
        voice=request.json.get('voice', 'Ana Florence')
    )
    
    # Store job ID with book
    store_audiobook_job(book_id, job_id)
    
    return jsonify({
        "job_id": job_id,
        "message": "Audiobook generation started"
    })

@app.route('/books/<int:book_id>/audiobook/status')
def audiobook_status(book_id):
    job_id = get_audiobook_job_id(book_id)
    if job_id:
        status = audio_connector.check_status(job_id)
        return jsonify(status)
    return jsonify({"error": "No audiobook generation in progress"})
```

### Django Integration
```python
from django.http import JsonResponse
from django.views import View
from bookshelf_integration import BookshelfConnector

class AudiobookGenerationView(View):
    def __init__(self):
        self.connector = BookshelfConnector("http://localhost:5000")
    
    def post(self, request, book_id):
        book = Book.objects.get(id=book_id)
        
        job_id = self.connector.generate_audiobook(
            book_text=book.content,
            book_title=book.title,
            voice=request.data.get('voice', 'Ana Florence')
        )
        
        # Create audiobook record
        AudiobookGeneration.objects.create(
            book=book,
            job_id=job_id,
            status='pending'
        )
        
        return JsonResponse({"job_id": job_id})
```

## Architecture Notes

### Job Management
- **Threading**: Background processing using Python threading
- **Job Storage**: In-memory job status tracking
- **Progress Updates**: Real-time progress via callback system
- **Error Handling**: Comprehensive error capture and reporting

### API Design
- **RESTful**: Standard REST endpoints for easy integration
- **Stateless**: Each request contains necessary information
- **Async Support**: Non-blocking job creation with status polling
- **File Serving**: Direct file downloads for generated audio

### Performance Considerations
- **Background Processing**: Jobs run in separate threads
- **Memory Management**: Jobs cleaned up after completion
- **Concurrent Requests**: Multiple simultaneous job support
- **Resource Limits**: Consider implementing job queues for high load

## Configuration

### Environment Variables
```bash
# API server configuration
export AUDIOBOOK_API_HOST="0.0.0.0"
export AUDIOBOOK_API_PORT="5000"
export AUDIOBOOK_OUTPUT_DIR="./audiobooks"

# TTS model configuration
export TTS_MODEL="tts_models/multilingual/multi-dataset/xtts_v2"
```

### Production Deployment
```python
# Use production WSGI server
from bookshelf_integration import create_app
import gunicorn

app = create_app(output_dir="/var/audiobooks")

# gunicorn config
bind = "0.0.0.0:5000"
workers = 4
timeout = 300  # 5 minutes for long generations
```

## Security Considerations

1. **Input Validation**: Validate file paths and text input
2. **File Access**: Restrict file access to designated directories
3. **Rate Limiting**: Consider implementing rate limiting for API endpoints
4. **Authentication**: Add authentication for production use
5. **CORS**: Configure CORS headers for cross-origin requests

## Error Handling

### Common Error Responses
```json
{
  "error": "Job not found",
  "status": "error"
}
```

### Status Values
- `pending`: Job created, waiting to start
- `processing`: Audiobook generation in progress
- `completed`: Generation successful
- `failed`: Generation failed with error

### Error Recovery
- Failed jobs remain in system for debugging
- Detailed error messages in job status
- Automatic cleanup of failed job files