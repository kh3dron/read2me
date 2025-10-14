from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:9970"}})

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:postgres@localhost:5432/postgres"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["CORS_HEADERS"] = "Content-Type"

db = SQLAlchemy(app)
auth = HTTPBasicAuth()

DATA_ROOT = "/data"


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user


@app.route("/login", methods=["GET"])
@auth.login_required
def login():
    return jsonify({"message": "Logged in successfully"})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"message": "OK"})


@app.route("/api/v1/files", methods=["GET"])
@auth.login_required
def files():
    try:
        path = request.args.get("path", "")
        full_path = f"data/{path}"

        # Ensure the path is valid and exists
        if not os.path.exists(full_path):
            print("Path does not exist or is invalid")
            return jsonify({"error": "Path does not exist or is invalid"}), 404

        # List files in the specified directory
        files = os.listdir(f"data/{path}")
        files.sort()

        # Prepare the response data
        response_data = {
            "path": full_path,
            "contents": [
                {
                    "name": file,
                    "size": os.path.getsize(f"data/{path}/{file}"),
                    "type": "file",
                }
                for file in files
            ],
        }

        return jsonify(response_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9930)
