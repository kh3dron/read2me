from flask import Flask
from flask import jsonify
import os
from flask import send_file

app = Flask(__name__)

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
#TODO send as json 
@app.route("/api/v1/<name>/transcriptions", methods=["GET"])
def name_transcriptions(name):
    return send_file(f"data/audio/{name}/metadata.txt")

# # get track
# @app.route("/api/v1/<name>/<track>", methods=["GET"])
# def name_track(name, track):
#     return send_file(f"data/audio/{name}/wavs/{track}")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9930)