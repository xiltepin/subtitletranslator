#!/usr/bin/env python3
"""
Subtitle Translator using Ollama - with beautiful progress bar
"""

import argparse
import os
import re
import requests
import time
from pathlib import Path
from typing import List
from tqdm import tqdm  # <-- New import

# Configuration
OLLAMA_HOST = "192.168.0.6"
OLLAMA_PORT = 11434
DEFAULT_MODEL = "qwen2.5:14b"
MEDIA_SERVER = "192.168.0.2"
MEDIA_BASE = "Media"

# Debug flag
DEBUG = True


def debug_print(message: str):
    if DEBUG:
        timestamp = time.strftime("%H:%M:%S")
        print(f"[DEBUG {timestamp}] {message}")


class SubtitleEntry:
    def __init__(self, index: int, timestamp: str, text: str):
        self.index = index
        self.timestamp = timestamp
        self.text = text


def parse_srt(content: str) -> List[SubtitleEntry]:
    debug_print("Starting SRT parsing...")
    entries = []
    blocks = content.strip().split('\n\n')
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            try:
                index = int(lines[0])
                timestamp = lines[1]
                text = '\n'.join(lines[2:])
                entries.append(SubtitleEntry(index, timestamp, text))
            except ValueError:
                continue
    debug_print(f"Parsed {len(entries)} entries")
    return entries


def test_ollama_connection(model: str) -> bool:
    try:
        url = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/tags"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        models = [m.get('name', '') for m in response.json().get('models', [])]
        if model not in models:
            print(f"Warning: Model '{model}' not available")
            return False
        return True
    except Exception as e:
        print(f"Error connecting to Ollama: {e}")
        return False


def translate_text(text: str, target_lang: str, model: str, source_lang: str = "auto") -> str:
    url = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/generate"
    
    lang_names = {
        'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
        'it': 'Italian', 'pt': 'Portuguese', 'ja': 'Japanese', 'zh': 'Chinese',
        'ko': 'Korean', 'ru': 'Russian', 'ar': 'Arabic'
    }
    target_lang_name = lang_names.get(target_lang, target_lang)
    
    prompt = f"""Translate this subtitle text to {target_lang_name}.

CRITICAL RULES:
- Output ONLY the translation
- No explanations or notes
- No source language text
- Preserve line breaks and number of lines

Text:
{text}

Translation:"""

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1, "top_p": 0.8, "num_predict": 500}
    }

    try:
        response = requests.post(url, json=payload, timeout=180)
        response.raise_for_status()
        translation = response.json().get('response', '').strip()
        
        # Clean up
        translation = re.sub(r'^(Translation|Note|.*translation\s*[:：]).*$\n?', '', translation, flags=re.MULTILINE | re.IGNORECASE)
        translation = re.sub(r'\n{3,}', '\n\n', translation.strip())
        return translation
    except Exception as e:
        debug_print(f"Translation error: {e}")
        return text


def build_network_path(relative_path: str) -> str:
    debug_print(f"Input path: {relative_path}")
    
    if relative_path.startswith('/mnt/media/') or relative_path.startswith('/'):
        debug_print("Already valid absolute path")
        return relative_path
    
    if '\\\\' in relative_path or MEDIA_SERVER in relative_path:
        relative_path = relative_path.lstrip('\\/').lstrip('\\\\')
        if MEDIA_BASE in relative_path:
            parts = relative_path.split(MEDIA_BASE, 1)
            if len(parts) > 1:
                relative_path = parts[1].lstrip('\\/').lstrip('\\\\')
        relative_path = relative_path.replace('\\', '/')
        full_path = f"/mnt/media/{relative_path}"
        debug_print(f"Converted network path: {full_path}")
        return full_path
    
    full_path = str(Path(relative_path).resolve())
    debug_print(f"Resolved relative path: {full_path}")
    return full_path


def extract_language_from_filename(filename: str) -> str:
    match = re.search(r'\.([a-z]{2})(?:\.[^.]+)?\.srt$', filename, re.IGNORECASE)
    return match.group(1) if match else "unknown"


def generate_output_filename(input_path: str, target_lang: str) -> str:
    output_path = re.sub(r'\.([a-z]{2})(?:\.[^.]+)?\.srt$', f'.{target_lang}.srt', input_path, flags=re.IGNORECASE)
    if output_path == input_path:
        output_path = input_path.replace('.srt', f'.{target_lang}.srt')
    return output_path


def translate_subtitle_file(input_path: str, target_lang: str, model: str, max_entries: int = None):
    print(f"\n{'='*60}")
    print(f"Subtitle Translation Started")
    print(f"{'='*60}")
    print(f"Input: {input_path}")
    print(f"Target: {target_lang.upper()}")
    print(f"Model: {model}")
    print(f"{'='*60}\n")

    if not test_ollama_connection(model):
        raise Exception("Model not available")

    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = parse_srt(content)
    if max_entries:
        entries = entries[:max_entries]
        print(f"TEST MODE: Processing first {max_entries} entries")

    print(f"Translating {len(entries)} subtitles...\n")

    translated_entries = []
    start_time = time.time()

    # Beautiful progress bar
    with tqdm(total=len(entries), desc="Translating", unit="line", colour="cyan") as pbar:
        for entry in entries:
            translated_text = translate_text(entry.text, target_lang, model)
            translated_entries.append(SubtitleEntry(entry.index, entry.timestamp, translated_text))
            pbar.update(1)

    total_time = time.time() - start_time
    print(f"\n✓ Complete! Translated in {total_time:.1f}s ({total_time/len(entries):.2f}s per line)")

    output_path = generate_output_filename(input_path, target_lang)
    with open(output_path, 'w', encoding='utf-8') as f:
        for e in translated_entries:
            f.write(f"{e.index}\n{e.timestamp}\n{e.text}\n\n")

    print(f"\nSaved: {output_path}")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description='Ollama Subtitle Translator')
    parser.add_argument('path', help='Path to .srt file')
    parser.add_argument('--lang', '-l', required=True, help='Target language')
    parser.add_argument('--model', '-m', default=DEFAULT_MODEL, help='Ollama model')
    parser.add_argument('--test', '-t', type=int, help='Test mode - first N entries')
    parser.add_argument('--no-debug', action='store_true', help='Disable debug')

    args = parser.parse_args()
    global DEBUG
    DEBUG = not args.no_debug

    full_path = build_network_path(args.path)
    if not os.path.exists(full_path):
        print(f"Error: File not found: {full_path}")
        return 1

    try:
        translate_subtitle_file(full_path, args.lang, args.model, args.test)
    except Exception as e:
        print(f"ERROR: {e}")
        if DEBUG:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())