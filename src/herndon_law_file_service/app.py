from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(
    os.getcwd(), "src", "herndon_law_file_service", "static")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
BASE_URL = "http://127.0.0.1:5000" if app.debug else "https://herndonlawfileservice.pythonanywhere.com"


@app.route("/")
def index():
    return "<h1>Herndon Law File Service</h1>"


@app.route("/file-upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"isError": True}), 400
    file = request.files["file"]

    file_extension = file.filename.split(".")[1]
    num_files = len(os.listdir(UPLOAD_FOLDER))
    filename = secure_filename(f"{num_files}.{file_extension}")
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    return jsonify({"isError": False, "url": f"{BASE_URL}/static/{filename}"}), 200
