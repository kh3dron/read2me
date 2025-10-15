"""
Bookshelf Integration Module for Read2Me
Simple web API wrapper for audiobook generation
"""

from flask import Flask, request, jsonify, send_file
from werkzeug.exceptions import BadRequest
import os
import json
import threading
from pathlib import Path
from typing import Dict, Optional
from ..lib.read2me_lib import AudiobookGenerator

class BookshelfAudioAPI:
    """Simple API wrapper for Bookshelf integration"""
    
    def __init__(self, output_dir: str = "audiobooks"):
        self.generator = AudiobookGenerator(output_dir=output_dir)
        self.active_jobs = {}  # job_id -> status/progress
        
    def create_job(self, text: str, title: str, voice: Optional[str] = None, 
                   voice_file: Optional[str] = None, language: str = "en") -> str:
        """Create audiobook generation job"""
        import uuid
        job_id = str(uuid.uuid4())
        
        # Initialize job status
        self.active_jobs[job_id] = {
            "status": "pending",
            "progress": "Job created",
            "title": title,
            "voice": voice or "default",
            "language": language,
            "result": None,
            "error": None
        }
        
        # Start generation in background thread
        thread = threading.Thread(
            target=self._generate_audiobook,
            args=(job_id, text, title, voice, voice_file, language)
        )
        thread.daemon = True
        thread.start()
        
        return job_id
    
    def create_job_from_file(self, file_path: str, voice: Optional[str] = None,
                           voice_file: Optional[str] = None, language: str = "en") -> str:
        """Create audiobook generation job from file"""
        import uuid
        job_id = str(uuid.uuid4())
        
        file_path = Path(file_path)
        title = file_path.stem
        
        # Read file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            # Create failed job
            self.active_jobs[job_id] = {
                "status": "failed",
                "progress": f"Failed to read file: {e}",
                "title": title,
                "error": str(e)
            }
            return job_id
        
        return self.create_job(text, title, voice, voice_file, language)
    
    def get_job_status(self, job_id: str) -> Dict:
        """Get job status and progress"""
        if job_id not in self.active_jobs:
            return {"error": "Job not found"}
        return self.active_jobs[job_id]
    
    def get_job_result(self, job_id: str) -> Optional[str]:
        """Get job result file path"""
        if job_id not in self.active_jobs:
            return None
        
        job = self.active_jobs[job_id]
        if job["status"] == "completed" and job["result"]:
            return job["result"]["output_directory"]
        return None
    
    def list_voices(self) -> list:
        """List available voices"""
        return self.generator.get_available_voices()
    
    def _generate_audiobook(self, job_id: str, text: str, title: str, 
                          voice: Optional[str], voice_file: Optional[str], language: str):
        """Generate audiobook in background thread"""
        def progress_callback(message: str):
            if job_id in self.active_jobs:
                self.active_jobs[job_id]["progress"] = message
        
        try:
            self.active_jobs[job_id]["status"] = "processing"
            
            result = self.generator.create_audiobook(
                text=text,
                title=title,
                voice=voice,
                voice_file=voice_file,
                language=language,
                progress_callback=progress_callback
            )
            
            self.active_jobs[job_id]["status"] = "completed"
            self.active_jobs[job_id]["result"] = result
            self.active_jobs[job_id]["progress"] = "Completed successfully"
            
        except Exception as e:
            self.active_jobs[job_id]["status"] = "failed"
            self.active_jobs[job_id]["error"] = str(e)
            self.active_jobs[job_id]["progress"] = f"Failed: {e}"

# Flask app for web integration
def create_app(output_dir: str = "audiobooks") -> Flask:
    """Create Flask app for Bookshelf integration"""
    app = Flask(__name__)
    api = BookshelfAudioAPI(output_dir=output_dir)
    
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({"status": "ok"})
    
    @app.route('/voices', methods=['GET'])
    def list_voices():
        return jsonify({"voices": api.list_voices()})
    
    @app.route('/generate', methods=['POST'])
    def generate_audiobook():
        data = request.get_json()
        if not data or 'text' not in data or 'title' not in data:
            raise BadRequest("Missing required fields: text, title")
        
        job_id = api.create_job(
            text=data['text'],
            title=data['title'],
            voice=data.get('voice'),
            voice_file=data.get('voice_file'),
            language=data.get('language', 'en')
        )
        
        return jsonify({
            "job_id": job_id,
            "status": "pending",
            "message": "Audiobook generation started"
        })
    
    @app.route('/generate/file', methods=['POST'])
    def generate_from_file():
        data = request.get_json()
        if not data or 'file_path' not in data:
            raise BadRequest("Missing required field: file_path")
        
        job_id = api.create_job_from_file(
            file_path=data['file_path'],
            voice=data.get('voice'),
            voice_file=data.get('voice_file'),
            language=data.get('language', 'en')
        )
        
        return jsonify({
            "job_id": job_id,
            "status": "pending",
            "message": "Audiobook generation started"
        })
    
    @app.route('/status/<job_id>', methods=['GET'])
    def get_status(job_id):
        status = api.get_job_status(job_id)
        return jsonify(status)
    
    @app.route('/download/<job_id>', methods=['GET'])
    def download_audiobook(job_id):
        result_path = api.get_job_result(job_id)
        if not result_path:
            return jsonify({"error": "Audiobook not ready or job not found"}), 404
        
        # Return metadata file for download
        metadata_file = Path(result_path) / "metadata.json"
        if metadata_file.exists():
            return send_file(str(metadata_file))
        
        return jsonify({"error": "Audiobook files not found"}), 404
    
    @app.route('/download/<job_id>/chapter/<int:chapter_num>', methods=['GET'])
    def download_chapter(job_id, chapter_num):
        result_path = api.get_job_result(job_id)
        if not result_path:
            return jsonify({"error": "Audiobook not ready or job not found"}), 404
        
        # Find chapter file
        chapter_file = Path(result_path) / f"chapter_{chapter_num:02d}.wav"
        if chapter_file.exists():
            return send_file(str(chapter_file))
        
        return jsonify({"error": "Chapter not found"}), 404
    
    return app

# Example usage for Bookshelf integration
class BookshelfConnector:
    """Simple connector class for Bookshelf application"""
    
    def __init__(self, api_base_url: str = "http://localhost:5000"):
        self.api_base_url = api_base_url
    
    def generate_audiobook(self, book_text: str, book_title: str, 
                         voice: Optional[str] = None) -> str:
        """Generate audiobook and return job ID"""
        import requests
        
        response = requests.post(f"{self.api_base_url}/generate", json={
            "text": book_text,
            "title": book_title,
            "voice": voice
        })
        
        if response.status_code == 200:
            return response.json()["job_id"]
        else:
            raise Exception(f"API error: {response.text}")
    
    def check_status(self, job_id: str) -> Dict:
        """Check audiobook generation status"""
        import requests
        
        response = requests.get(f"{self.api_base_url}/status/{job_id}")
        return response.json()
    
    def get_available_voices(self) -> list:
        """Get list of available voices"""
        import requests
        
        response = requests.get(f"{self.api_base_url}/voices")
        return response.json()["voices"]

if __name__ == "__main__":
    # Run the Flask app
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)