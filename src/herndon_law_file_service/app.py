from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(
    os.getcwd(), "herndon-law-file-service", "src", "static")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
BASE_URL = "http://127.0.0.1:5000" if app.debug else "https://herndonlawfileservice.pythonanywhere.com"


@app.route("/")
def index():
    return "<h1>Herndon Law File Services</h1>"


@app.route("/file", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"isError": True}), 400
    file = request.files["file"]

    file_extension = file.filename.split(".")[1]
    num_files = len(os.listdir(UPLOAD_FOLDER)
                    ) if os.path.isdir(UPLOAD_FOLDER) else 0
    filename = secure_filename(f"{num_files}.{file_extension}")

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file.save(file_path)
    return jsonify({"isError": False, "url": f"{BASE_URL}/static/{filename}"}), 200


@app.route("/file/<file_name>", methods=["DELETE"])
def delete_file(file_name: str):
    file_path = os.path.join(UPLOAD_FOLDER, str(file_name))
    if not os.path.exists(file_path):
        return jsonify({"isError": True, "errorMessage": "File does not exist."}), 400
    os.remove(file_path)
    return jsonify({"isError": False})
