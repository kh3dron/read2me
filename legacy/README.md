# Legacy Components

This directory contains the original Read2Me implementation using Flask/Celery architecture. These components are deprecated in favor of the simplified modular design in `src/`.

## Files

### Core Application
- **`app.py`**: Original Flask web server with authentication
- **`celery_worker.py`**: Celery worker for async task processing
- **`start-celery.sh`**: Script to start Celery worker

### Service Files
- **`tts-api.service`**: Systemd service for Flask API
- **`celery.service`**: Systemd service for Celery worker

### Processing Scripts
- **`endpoints/`**: Directory with original processing scripts
  - `tts.py`: Generic TTS generation
  - `clone-voice.py`: Voice cloning functionality
  - `epub-to-chapters.py`: Book processing utilities
  - `poc.py`: Proof of concept scripts

## Original Architecture

The legacy system used a microservices approach:

1. **Flask API Server** (`app.py`):
   - HTTP Basic Auth authentication
   - RESTful endpoints for TTS and voice cloning
   - Task queue integration with Celery

2. **Celery Worker** (`celery_worker.py`):
   - Async processing of TTS generation
   - Redis broker for task distribution
   - Background job execution

3. **Processing Scripts** (`endpoints/`):
   - Standalone Python scripts for TTS operations
   - Command-line interface for each operation
   - Direct file output management

## Migration Notes

### From Legacy to New System

**Old Flask API endpoints:**
```
/api/v1/tts -> src/read2me/cli/read2me_cli.py tts
/api/v1/clone -> src/read2me/cli/read2me_cli.py book --voice-file
/api/v1/audio/* -> src/read2me/lib/ voice management
```

**Old Celery tasks:**
```python
# Legacy
from celery_worker import generate_tts
task = generate_tts.delay(input_file)

# New
from read2me_lib import AudiobookGenerator
generator = AudiobookGenerator()
result = generator.create_audiobook_from_file(input_file)
```

**Authentication removal:**
The new system removes the HTTP Basic Auth requirement. For production web integration, implement authentication in your web application layer.

## Why Legacy?

The original Flask/Celery system had several limitations:

1. **Complexity**: Required Redis, Celery, and Flask setup
2. **Authentication**: Hard-coded credentials in source code
3. **Scalability**: Single-threaded processing bottlenecks
4. **Maintenance**: Multiple services to manage and monitor
5. **Integration**: Complex setup for simple use cases

## Preservation

These files are preserved for:

1. **Reference**: Understanding the original implementation
2. **Migration**: Gradual transition from old to new system
3. **Features**: Some advanced features may still be in legacy code
4. **Debugging**: Troubleshooting existing deployments

## Usage (Deprecated)

If you need to run the legacy system:

```bash
# Start Redis
redis-server

# Start Celery worker
cd legacy/
./start-celery.sh

# Start Flask API
python app.py
```

**Note**: This approach is not recommended for new installations. Use the modern components in `src/` instead.

## Migration Path

1. **Assessment**: Identify current usage of legacy endpoints
2. **Mapping**: Map old API calls to new library methods
3. **Testing**: Verify equivalent functionality in new system
4. **Deployment**: Replace legacy services with new components
5. **Cleanup**: Remove legacy files after successful migration

For new projects, start directly with the components in `src/`.