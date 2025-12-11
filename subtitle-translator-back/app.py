# ~/tools/subtranslator/subtitle-translator-back/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import subprocess
import os
import requests
from pathlib import Path

app = Flask(__name__)
CORS(app, origins=["https://192.168.0.5", "http://192.168.0.6:4200", "http://localhost:4200"])
app.config['JWT_SECRET_KEY'] = 'super-secret-key-2025-change-in-prod'  # CHANGE THIS
jwt = JWTManager(app)

# CHANGE THIS PASSWORD
PASSWORD = "123456789"

OLLAMA_URL = "http://localhost:11434"

@app.route('/api/login', methods=['POST'])
def login():
    if request.json.get('password') == PASSWORD:
        token = create_access_token(identity="user")
        return jsonify(token=token)
    return jsonify(error="Wrong password"), 401


@app.route('/api/models', methods=['GET'])
@jwt_required()
def get_models():
    try:
        resp = requests.get(f"{OLLAMA_URL}/api/tags")
        models = [m['name'] for m in resp.json().get('models', [])]
        return jsonify(models=models)
    except:
        return jsonify(models=["gemma2:27b", "llama3.2:8b", "qwen2.5:14b"])  # fallback


@app.route('/api/tree', methods=['POST'])
@jwt_required()
def tree():
    data = request.get_json()
    rel_path = data.get('path', '').lstrip('/')
    full_path = Path("/mnt/media") / rel_path

    if not full_path.exists():
        return jsonify(error="Path not found"), 404
    if not full_path.is_dir():
        return jsonify(error="Not a directory"), 400

    items = []
    for p in sorted(full_path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
        if p.name.startswith('.'): 
            continue
        rel = str(p.relative_to(Path("/mnt/media")))
        items.append({
            "name": p.name + ("/" if p.is_dir() else ""),
            "path": rel,
            "isDir": p.is_dir(),
            "isSrt": p.suffix.lower() == ".srt"
        })
    return jsonify(items=items)


@app.route('/api/translate', methods=['POST'])
@jwt_required()
def translate():
    data = request.json
    srt_path = data.get('file')        # full path like "/mnt/media/Series/..."
    lang = data.get('lang')
    model = data.get('model')

    script = "/home/xiltepin/tools/subtranslator/subtitle-translator-ai/subtitle_translator.py"

    cmd = ["python", script, srt_path, "--lang", lang, "--model", model]

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        output_lines = []
        for line in proc.stdout:
            line = line.rstrip()
            output_lines.append(line)
            # Send progress via SSE would be ideal, but for simplicity we just collect
            # (Angular will poll or we can upgrade later)

        proc.wait()
        if proc.returncode != 0:
            return jsonify(error="".join(output_lines)), 500

        return jsonify(success=True, output="\n".join(output_lines))
    except Exception as e:
        return jsonify(error=str(e)), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)