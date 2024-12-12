from flask import Flask
from flask import jsonify
import os
from flask import send_file, request
from flask_cors import CORS, cross_origin
import json
import requests
from celery_worker import clone_voice

app = Flask(__name__)
cors = CORS(app) # allow CORS for all domains on all routes.
app.config['CORS_HEADERS'] = 'Content-Type'



@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/health")
def health():
    return "<p>OK</p>"


# 
# APIs for getting files from the data store
# 

# list names
@app.route("/api/v1/names", methods=["GET"])
def names():
    names = os.listdir("data/audio/")
    names.sort()
    return jsonify(names)

# tracks of name
@app.route("/api/v1/<name>/tracks", methods=["GET"])
def name_tracks(name):
    tracks = os.listdir(f"data/audio/{name}/wavs")
    tracks.sort()
    return jsonify(tracks)

# transcript file
@app.route("/api/v1/<name>/transcriptions", methods=["GET"])
def name_transcriptions(name):
    return send_file(f"data/audio/{name}/metadata.json")

# tree transcripts
@app.route("/api/v1/tree", methods=["GET"])
def tree():
    tree = {}
    for name in os.listdir("data/audio/"):
        # Read the metadata.json file for each name
        with open(f"data/audio/{name}/metadata.json", 'r') as f:
            tree[name] = json.loads(f.read())
    return jsonify(tree)

# get track
@app.route("/api/v1/<name>/<track>", methods=["GET"])
def get_track(name, track):
    print(f"data/audio/{name}/wavs/{track}.wav")
    return send_file(f"data/audio/{name}/wavs/{track}.wav")

# get track transcription
@app.route("/api/v1/<name>/<track>/transcription", methods=["GET"])
def get_track_transcription(name, track):
    # get the transcription from the metadata.json file
    with open(f"data/audio/{name}/metadata.json", 'r') as f:
        metadata = json.loads(f.read())
    return jsonify(metadata[track])

#
# Voice Cloning
#
@app.route("/api/v1/clone", methods=["POST"])
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
def get_clone_result(task_id):
    output_path = f"output/{task_id}.wav"
    if os.path.exists(output_path):
        return send_file(output_path)
    return jsonify({"error": "File not found"}), 404

#
# Retrieving 
#

@app.route("/api/v1/retrieve/<task_id>")
def retrieve(task_id):
    output_path = f"output/{task_id}.wav"
    if os.path.exists(output_path):
        return send_file(output_path)
    return jsonify({"error": "File not found"}), 404

@app.route("/api/v1/retrieve")
def retrieve_all():
    files = os.listdir("output")
    return jsonify(files)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9930)