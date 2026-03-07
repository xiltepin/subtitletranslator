from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import subprocess
import os
import re
import time
import json
import requests

app = Flask(__name__)
CORS(app)

# Configuración
MEDIA_MOUNT = '/mnt/media'
TRANSLATE_SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), './translate.sh'))
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://host.docker.internal:11434')

# ==================== LISTAR ARCHIVOS .SRT ====================
@app.route('/api/files', methods=['GET'])
def list_files():
    start_time = time.time()
    try:
        base_paths = [
            os.path.join(MEDIA_MOUNT, 'Series'),
            os.path.join(MEDIA_MOUNT, 'Movies')
        ]
        # Usar 'find' nativo es mucho más rápido que os.walk sobre NFS
        existing_paths = [p for p in base_paths if os.path.exists(p)]
        if not existing_paths:
            return jsonify([])

        cmd = ['find'] + existing_paths + [
            '-name', '*.srt', '-type', 'f',
            '-not', '-path', '*/#recycle/*',
            '-not', '-path', '*/Temp/*',
            '-not', '-path', '*/Tools/*',
            '-not', '-path', '*/PersonalVideos/*'
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        srt_files = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            full_path = line.strip()
            file_name = os.path.basename(full_path)
            rel_path = os.path.relpath(full_path, MEDIA_MOUNT)
            srt_files.append({
                'path': full_path,
                'name': file_name,
                'relative': rel_path.replace(os.sep, '/')
            })
        
        srt_files.sort(key=lambda x: x['relative'].lower())
        elapsed = time.time() - start_time
        count = len(srt_files)
        print(f"\n✅ LISTA DE ARCHIVOS CARGADA EXITOSAMENTE")
        print(f"   📁 Archivos .srt encontrados: {count}")
        print(f"   ⏱️  Tiempo de carga: {elapsed:.2f} segundos")
        print(f"   📍 Rutas escaneadas: {', '.join(existing_paths)}\n")
        return jsonify(srt_files)
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n❌ ERROR AL CARGAR LISTA DE ARCHIVOS ({elapsed:.2f}s): {str(e)}\n")
        return jsonify({'error': str(e)}), 500


# ==================== LISTAR MODELOS OLLAMA ====================
@app.route('/api/models', methods=['GET'])
def get_models():
    try:
        response = requests.get(f'{OLLAMA_HOST}/api/tags', timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = [model['name'] for model in data.get('models', [])]
            print(f"📋 Modelos Ollama disponibles: {models}")
            return jsonify(models)
        return jsonify([])
    except Exception as e:
        print(f"❌ Error listando modelos Ollama: {e}")
        return jsonify([])


# ==================== TRADUCCIÓN CON PROGRESO EN TIEMPO REAL ====================

@app.route('/api/translate', methods=['GET'])
def translate():
    file_path = request.args.get('path')
    lang = request.args.get('lang')
    context = request.args.get('context', '')
    model = request.args.get('model', 'gemma3:12b')
    test_str = request.args.get('test')
    test = int(test_str) if test_str else None

    if not file_path or not lang:
        return 'Faltan parámetros path o lang', 400
    if not os.path.exists(file_path):
        return 'Archivo no encontrado', 404

    cmd = ['bash', '-u', TRANSLATE_SCRIPT, file_path, '--lang', lang]
    if model != 'gemma3:12b':
        cmd.extend(['--model', model])
    if context.strip():
        cmd.extend(['--context', context.strip()])
    if test is not None:
        cmd.extend(['--test', str(test)])

    def generate():
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
                cwd=os.path.dirname(TRANSLATE_SCRIPT)
            )

            # Eventos iniciales inmediatos
            print("Traducción iniciada con Ollama...")
            yield f"data: {json.dumps({'type': 'log', 'message': 'Traducción iniciada con Ollama...'})}\n\n"
            print("Progreso: 0%")
            yield f"data: {json.dumps({'type': 'progress', 'percent': 0})}\n\n"

            # Bucle único para leer todo el output en tiempo real
            for line in process.stdout:
                line = line.rstrip('\n')
                if line:
                    print(line)
                    yield f"data: {json.dumps({'type': 'log', 'message': line})}\n\n"

                    match = re.search(r'(\d+)%\|', line)
                    if match:
                        percent = int(match.group(1))
                        print(f"Progreso: {percent}%")
                        yield f"data: {json.dumps({'type': 'progress', 'percent': percent})}\n\n"

            process.wait()

            if process.returncode == 0:
                dir_name = os.path.dirname(file_path)
                base_name = os.path.basename(file_path)
                output_name = re.sub(r'\.([a-z]{2})(?:\.[^.]+)?\.srt$', f'.{lang}.srt', base_name, flags=re.IGNORECASE)
                if output_name == base_name:
                    output_name = base_name.replace('.srt', f'.{lang}.srt')
                output_path = os.path.join(dir_name, output_name)

                print('¡Traducción completada!')
                yield f"data: {json.dumps({'type': 'log', 'message': '¡Traducción completada!'})}\n\n"
                print('Progreso: 100%')
                yield f"data: {json.dumps({'type': 'progress', 'percent': 100})}\n\n"
                print(f'Archivo generado: {output_path}')
                yield f"data: {json.dumps({'type': 'complete', 'output_file': output_path})}\n\n"
            else:
                print(f"Falló con código {process.returncode}")
                yield f"data: {json.dumps({'type': 'error', 'message': f'Falló con código {process.returncode}'})}\n\n"

        except Exception as e:
            print(f"Error: {e}")
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    # ¡ESTA LÍNEA ES OBLIGATORIA!
    return Response(generate(), mimetype='text/event-stream')

# ==================== LEER README ====================
@app.route('/api/readme', methods=['GET'])
def get_readme():
    readme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'readme.md'))
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({'content': content})
    except Exception as e:
        return jsonify({'content': f'Error leyendo README: {str(e)}'})


# ==================== INICIO DEL SERVIDOR ====================
if __name__ == '__main__':
    print("🚀 Subtitle Translator AI - Backend Flask")
    print(f"Media mount: {MEDIA_MOUNT}")
    print(f"Translate script: {TRANSLATE_SCRIPT}")
    print(f"Ollama host: {OLLAMA_HOST}")
    app.run(host='0.0.0.0', port=5001, debug=True)
