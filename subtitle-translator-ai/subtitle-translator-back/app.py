from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import re

app = Flask(__name__)
CORS(app)

MEDIA_MOUNT = '/mnt/media'
TRANSLATE_SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../translate.sh'))

@app.route('/api/files', methods=['GET'])
def list_files():
    srt_files = []
    try:
        for root, _, files in os.walk(MEDIA_MOUNT):
            for file in files:
                if file.lower().endswith('.srt'):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, MEDIA_MOUNT)
                    srt_files.append({
                        'path': full_path,
                        'name': file,
                        'relative': rel_path.replace(os.sep, '/')
                    })
        srt_files.sort(key=lambda x: x['relative'].lower())
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return jsonify(srt_files)

@app.route('/api/translate', methods=['POST'])
def translate():
    data = request.json
    file_path = data.get('path')
    lang = data.get('lang')
    context = data.get('context', '')
    model = data.get('model', 'gemma2:27b')
    test = data.get('test')

    if not file_path or not lang:
        return jsonify({'error': 'path y lang requeridos'}), 400
    if not os.path.exists(file_path):
        return jsonify({'error': 'Archivo no encontrado'}), 404

    cmd = [TRANSLATE_SCRIPT, file_path, '--lang', lang]
    if model != 'gemma2:27b':
        cmd.extend(['--model', model])
    if context.strip():
        cmd.extend(['--context', context.strip()])
    if test is not None:
        cmd.extend(['--test', str(test)])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(TRANSLATE_SCRIPT))
        output = result.stdout + result.stderr

        if result.returncode != 0:
            return jsonify({'error': 'Error en traducción', 'details': output}), 500

        dir_name = os.path.dirname(file_path)
        base_name = os.path.basename(file_path)
        output_name = re.sub(r'\.([a-z]{2})(?:\.[^.]+)?\.srt$', f'.{lang}.srt', base_name, flags=re.IGNORECASE)
        if output_name == base_name:
            output_name = base_name.replace('.srt', f'.{lang}.srt', 1)
        output_path = os.path.join(dir_name, output_name)

        return jsonify({
            'success': True,
            'output': output,
            'output_file': output_path if os.path.exists(output_path) else None
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/models', methods=['GET'])
def get_models():
    try:
        result = subprocess.run(['ollama', 'ls'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            lines = [l for l in result.stdout.strip().split('\n') if l.strip()]
            models = [line.split()[0] for line in lines[1:]] if len(lines) > 1 else []
            return jsonify(models)
        return jsonify([])
    except:
        return jsonify([])

@app.route('/api/readme', methods=['GET'])
def get_readme():
    readme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../readme.md'))
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            return jsonify({'content': f.read()})
    except:
        return jsonify({'content': 'README no encontrado'})

if __name__ == '__main__':
    print("🚀 Subtitle Translator AI - Backend Flask")
    print(f"Media mount: {MEDIA_MOUNT}")
    print(f"Translate script: {TRANSLATE_SCRIPT}")
    app.run(host='0.0.0.0', port=5000, debug=True)
