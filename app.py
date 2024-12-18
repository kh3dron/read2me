from flask import Flask
from flask import jsonify
import os
from flask import send_file, request
from flask_cors import CORS, cross_origin
import json
import requests
from celery_worker import clone_voice
import logging
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
cors = CORS(app) # allow CORS for all domains on all routes.
app.config['CORS_HEADERS'] = 'Content-Type'

# Add authentication setup
auth = HTTPBasicAuth()

# Replace these with your desired username/password
users = {
    "admin": generate_password_hash("#4TurkeyTom")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username
    return None

@app.route("/health")
@auth.login_required
def health():
    return "<p>OK</p>"

@app.route("/api/v1/audio/names", methods=["GET"])
@auth.login_required
def names():
    try:
        if not os.path.exists("data/audio/"):
            return jsonify({"error": "Audio directory not found"}), 404
        names = os.listdir("data/audio/")
        names.sort()
        return jsonify(names)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/v1/audio/<name>/tracks", methods=["GET"])
@auth.login_required
def name_tracks(name):
    try:
        path = f"data/audio/{name}/wavs"
        if not os.path.exists(path):
            return jsonify({"error": f"Tracks not found for {name}"}), 404
        tracks = os.listdir(path)
        tracks.sort()
        return jsonify(tracks)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/v1/audio/<name>/transcriptions", methods=["GET"])
@auth.login_required
def name_transcriptions(name):
    try:
        path = f"data/audio/{name}/metadata.json"
        if not os.path.exists(path):
            return jsonify({"error": f"Transcriptions not found for {name}"}), 404
        return send_file(path)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/v1/audio/tree", methods=["GET"])
@auth.login_required
def tree():
    tree = {}
    for name in os.listdir("data/audio/"):
        # Read the metadata.json file for each name
        with open(f"data/audio/{name}/metadata.json", 'r') as f:
            tree[name] = json.loads(f.read())
    return jsonify(tree)

@app.route("/api/v1/audio/<name>/<track>", methods=["GET"])
@auth.login_required
def get_track(name, track):
    print(f"data/audio/{name}/wavs/{track}.wav")
    return send_file(f"data/audio/{name}/wavs/{track}.wav")

# get track transcription

@app.route("/api/v1/audio/<name>/<track>/transcription", methods=["GET"])
@auth.login_required
def get_track_transcription(name, track):
    # get the transcription from the metadata.json file
    with open(f"data/audio/{name}/metadata.json", 'r') as f:
        metadata = json.loads(f.read())
    return jsonify(metadata[track])

# Voice Cloning

@app.route("/api/v1/clone", methods=["POST"])
@auth.login_required
def clone():
    name = request.form["name"]
    source_filename = request.form["source_filename"]
    input_text = request.form["input_text"]
    
    # Launch async task
    task = clone_voice.delay(name, source_filename, input_text)
    
    return jsonify({
        "status": "processing",
        "task_id": task.id
    })

@app.route("/api/v1/clone/status/<task_id>")
@auth.login_required
def clone_status(task_id):
    task = clone_voice.AsyncResult(task_id)
    if task.ready():
        result = task.get()
        return jsonify({
            "status": "completed",
            "result": result
        })
    return jsonify({
        "status": "processing"
    })

@app.route("/api/v1/clone/result/<task_id>")
@auth.login_required
def get_clone_result(task_id):
    output_path = f"output/{task_id}.wav"
    if os.path.exists(output_path):
        return send_file(output_path)
    return jsonify({"error": "File not found"}), 404

# Retrieving tasks and audio generations

@app.route("/api/v1/retrieve/<task_id>")
@auth.login_required
def retrieve(task_id):
    output_path = f"output/{task_id}.wav"
    if os.path.exists(output_path):
        return send_file(output_path)
    return jsonify({"error": "File not found"}), 404

@app.route("/api/v1/retrieve")
@auth.login_required
def retrieve_all():
    with open("generation_log.json", "r") as f:
        log_data = json.load(f)
    return jsonify(log_data)

@app.route("/api/v1/books")
@auth.login_required
def list_books():
    logger.debug("Starting list_books function")
    try:
        if not os.path.exists("data/split_books/"):
            logger.error("Directory not found")
            return jsonify({"error": "Books directory not found"}), 404
        books = os.listdir("data/split_books/")
        logger.debug(f"Found books: {books}")
        books.sort()
        return jsonify(books)
    except Exception as e:
        logger.error(f"Error in list_books: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/v1/books/<book_name>")
@auth.login_required
def book(book_name):
    try:
        book_path = f"data/split_books/{book_name}"
        print(book_path)
        if not os.path.exists(book_path):
            return jsonify({"error": "Book not found"}), 404
            
        chapters = os.listdir(book_path)
        chapters.sort()  # Sort chapters for consistent ordering
        return jsonify(chapters)
    except Exception as e:
        logger.error(f"Error in book: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9930)