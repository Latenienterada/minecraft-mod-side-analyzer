from flask import Flask, request, jsonify
import os
from analyzer import analyze_mod

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/analyze", methods=["POST"])
def analyze():
    if "mod" not in request.files:
        return jsonify({"error": "No se subió ningún archivo"}), 400

    file = request.files["mod"]

    if not file.filename.endswith(".jar"):
        return jsonify({"error": "El archivo no es un .jar"}), 400

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    result = analyze_mod(path)

    os.remove(path)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
