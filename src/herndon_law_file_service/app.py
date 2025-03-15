from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import uuid

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(
    os.getcwd(), "src", "herndon_law_file_service", "static")
BASE_URL = "http://127.0.0.1:5000" if app.debug else "https://herndonlawfileservice.pythonanywhere.com"


@app.route("/")
def index():
    return "<h1>Herndon Law File Service</h1>"


@app.route("/file", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"isError": True}), 400
    file = request.files["file"]

    file_extension = file.filename.split(".")[1]
    filename = secure_filename(f"{uuid.uuid4()}.{file_extension}")

    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return jsonify({"isError": False, "url": f"{BASE_URL}/static/{filename}"}), 200


@app.route("/file/<file_name>", methods=["DELETE"])
def delete_file(file_name: str):
    file_path = os.path.join(UPLOAD_FOLDER, str(file_name))
    if not os.path.exists(file_path):
        return jsonify({"isError": True, "errorMessage": "File does not exist."}), 400
    os.remove(file_path)
    return jsonify({"isError": False})
