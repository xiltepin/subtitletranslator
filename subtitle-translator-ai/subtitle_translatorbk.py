#!/usr/bin/env python3
"""
Subtitle Translator using Ollama
Translates SRT subtitle files using Ollama API
"""

import argparse
import os
import re
import requests
import time
from pathlib import Path
from typing import List, Tuple

# Configuration
OLLAMA_HOST = "192.168.0.6"
OLLAMA_PORT = 11434
DEFAULT_MODEL = "qwen2.5:14b"
MEDIA_SERVER = "192.168.0.2"
MEDIA_BASE = "Media"

# Debug flag
DEBUG = True


def debug_print(message: str):
    """Print debug messages"""
    if DEBUG:
        timestamp = time.strftime("%H:%M:%S")
        print(f"[DEBUG {timestamp}] {message}")


class SubtitleEntry:
    """Represents a single subtitle entry"""
    def __init__(self, index: int, timestamp: str, text: str):
        self.index = index
        self.timestamp = timestamp
        self.text = text


def parse_srt(content: str) -> List[SubtitleEntry]:
    """Parse SRT file content into subtitle entries"""
    debug_print("Starting SRT parsing...")
    entries = []
    blocks = content.strip().split('\n\n')
    debug_print(f"Found {len(blocks)} blocks in SRT file")
    
    for i, block in enumerate(blocks):
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            try:
                index = int(lines[0])
                timestamp = lines[1]
                text = '\n'.join(lines[2:])
                entries.append(SubtitleEntry(index, timestamp, text))
            except ValueError as e:
                debug_print(f"Warning: Could not parse block {i}: {e}")
                continue
    
    debug_print(f"Successfully parsed {len(entries)} subtitle entries")
    return entries


def test_ollama_connection(model: str) -> bool:
    """Test if Ollama is accessible and model is available"""
    debug_print(f"Testing connection to Ollama at {OLLAMA_HOST}:{OLLAMA_PORT}")
    
    try:
        url = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/tags"
        debug_print(f"Checking available models at {url}")
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        models = response.json().get('models', [])
        model_names = [m.get('name', '') for m in models]
        debug_print(f"Available models: {', '.join(model_names)}")
        
        if model not in model_names:
            print(f"Warning: Model '{model}' not found in available models")
            print(f"Available models: {', '.join(model_names)}")
            return False
        
        debug_print(f"✓ Model '{model}' is available")
        return True
        
    except requests.exceptions.ConnectionError:
        print(f"Error: Cannot connect to Ollama at {OLLAMA_HOST}:{OLLAMA_PORT}")
        print("Make sure Ollama is running on that host")
        return False
    except Exception as e:
        print(f"Error testing Ollama connection: {e}")
        return False


def translate_text(text: str, target_lang: str, model: str, source_lang: str = "auto") -> str:
    """Translate text using Ollama API"""
    url = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/generate"
    
    lang_names = {
        'en': 'English',
        'es': 'Spanish', 
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'ja': 'Japanese',
        'zh': 'Chinese',
        'ko': 'Korean',
        'ru': 'Russian',
        'ar': 'Arabic'
    }
    
    target_lang_name = lang_names.get(target_lang, target_lang)
    
    prompt = f"""Translate this subtitle text to {target_lang_name}.

CRITICAL RULES - FOLLOW EXACTLY:
1. Output ONLY the {target_lang_name} translation
2. NO explanations, notes, comments, or annotations
3. NO Chinese characters unless translating to Chinese
4. NO translation notes like "Translation note:" or "注："
5. NO alternative suggestions or variations
6. Keep the same number of lines as the original
7. Preserve line breaks exactly as they appear
8. Do not add any extra text before or after the translation

Original text:
{text}

{target_lang_name} translation:"""
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "top_p": 0.8,
            "num_predict": 150
        }
    }
    
    try:
        debug_print(f"Sending translation request (text length: {len(text)} chars)")
        start_time = time.time()
        
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        
        elapsed = time.time() - start_time
        debug_print(f"Translation received in {elapsed:.2f}s")
        
        result = response.json()
        translation = result.get('response', '').strip()
        
        # Clean up common issues
        translation = translation.replace('Translation:', '').strip()
        translation = translation.replace(f'{target_lang_name} translation:', '').strip()
        
        # Remove translation notes in various languages
        translation = re.sub(r'Translation note:.*?(?=\n|$)', '', translation, flags=re.IGNORECASE)
        translation = re.sub(r'Note:.*?(?=\n|$)', '', translation, flags=re.IGNORECASE)
        translation = re.sub(r'注：.*?(?=\n|$)', '', translation)
        translation = re.sub(r'注释：.*?(?=\n|$)', '', translation)
        translation = re.sub(r'說明：.*?(?=\n|$)', '', translation)
        
        # Remove leading/trailing whitespace
        translation = re.sub(r'^\s+', '', translation)
        translation = re.sub(r'\s+$', '', translation)
        translation = re.sub(r'\n{3,}', '\n\n', translation)
        
        debug_print(f"Translation result length: {len(translation)} chars")
        return translation
        
    except requests.exceptions.Timeout:
        print(f"Timeout translating text. The model may be overloaded.")
        return text
    except Exception as e:
        debug_print(f"Error translating: {e}")
        return text


def build_network_path(relative_path: str) -> str:
    """Build full path from relative path - works with WSL mount paths"""
    debug_print(f"Input path: {relative_path}")
    
    # If it's already a full WSL mount path, use it directly
    if relative_path.startswith('/mnt/'):
        debug_print("Already a WSL mount path, using as-is")
        return relative_path
    
    # If it's already an absolute Linux path, use it
    if relative_path.startswith('/'):
        debug_print("Already an absolute path, using as-is")
        return relative_path
    
    debug_print("Building WSL mount path from relative path")
    
    # Remove leading slashes and backslashes
    relative_path = relative_path.lstrip('\\/').lstrip('\\\\')
    
    # If path contains the server address, extract only the part after Media
    if MEDIA_SERVER in relative_path or f"\\\\{MEDIA_SERVER}" in relative_path:
        debug_print("Path contains server address, extracting relative part")
        if MEDIA_BASE in relative_path:
            parts = relative_path.split(MEDIA_BASE, 1)
            if len(parts) > 1:
                relative_path = parts[1].lstrip('\\/').lstrip('\\\\')
                debug_print(f"Extracted: {relative_path}")
    
    # Convert backslashes to forward slashes for Linux
    relative_path = relative_path.replace('\\', '/')
    
    # Build full WSL mount path
    full_path = f"/mnt/media/{relative_path}"
    debug_print(f"Final path: {full_path}")
    return full_path


def extract_language_from_filename(filename: str) -> str:
    """Extract language code from filename"""
    match = re.search(r'\.([a-z]{2})(?:\.[^.]+)?\.srt$', filename, re.IGNORECASE)
    if match:
        lang = match.group(1)
        debug_print(f"Extracted language code: {lang}")
        return lang
    debug_print("No language code found in filename")
    return "unknown"


def generate_output_filename(input_path: str, target_lang: str) -> str:
    """Generate output filename by replacing language code"""
    debug_print(f"Generating output filename with target lang: {target_lang}")
    
    output_path = re.sub(
        r'\.([a-z]{2})(?:\.[^.]+)?\.srt$',
        f'.{target_lang}.srt',
        input_path,
        flags=re.IGNORECASE
    )
    
    if output_path == input_path:
        output_path = input_path.replace('.srt', f'.{target_lang}.srt')
    
    debug_print(f"Output filename: {output_path}")
    return output_path


def translate_subtitle_file(input_path: str, target_lang: str, model: str, max_entries: int = None):
    """Translate entire subtitle file"""
    print(f"\n{'='*60}")
    print(f"Subtitle Translation Job Started")
    print(f"{'='*60}")
    print(f"Input file: {input_path}")
    print(f"Target language: {target_lang}")
    print(f"Model: {model}")
    print(f"{'='*60}\n")
    
    if not test_ollama_connection(model):
        raise Exception("Cannot connect to Ollama or model not available")
    
    debug_print("Reading subtitle file...")
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        debug_print(f"File read successfully ({len(content)} chars)")
    except UnicodeDecodeError:
        debug_print("UTF-8 decoding failed, trying alternative encodings...")
        for encoding in ['latin-1', 'cp1252', 'iso-8859-1']:
            try:
                debug_print(f"Trying encoding: {encoding}")
                with open(input_path, 'r', encoding=encoding) as f:
                    content = f.read()
                debug_print(f"Successfully decoded with {encoding}")
                break
            except:
                continue
        else:
            raise Exception("Could not decode subtitle file with any common encoding")
    
    entries = parse_srt(content)
    total_entries = len(entries)
    
    if max_entries:
        entries = entries[:max_entries]
        print(f"Processing first {max_entries} entries (test mode)")
    
    print(f"Found {total_entries} subtitle entries")
    
    source_lang = extract_language_from_filename(input_path)
    print(f"Source language: {source_lang}")
    print(f"Target language: {target_lang}\n")
    
    translated_entries = []
    start_time = time.time()
    
    for i, entry in enumerate(entries, 1):
        percent = (i / len(entries)) * 100
        elapsed = time.time() - start_time
        avg_time = elapsed / i
        remaining = avg_time * (len(entries) - i)
        
        print(f"Translating [{i}/{len(entries)}] ({percent:.1f}%) | "
              f"Elapsed: {elapsed:.0f}s | ETA: {remaining:.0f}s", end='\r')
        
        translated_text = translate_text(entry.text, target_lang, model, source_lang)
        translated_entries.append(SubtitleEntry(entry.index, entry.timestamp, translated_text))
    
    total_time = time.time() - start_time
    print(f"\n\n✓ Translation complete in {total_time:.0f}s ({total_time/60:.1f} min)")
    print(f"  Average: {total_time/len(entries):.2f}s per entry")
    
    debug_print("Generating output content...")
    output_content = []
    for entry in translated_entries:
        output_content.append(f"{entry.index}\n{entry.timestamp}\n{entry.text}\n")
    
    output_path = generate_output_filename(input_path, target_lang)
    
    print(f"\nWriting translated subtitles to:")
    print(f"  {output_path}")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_content))
    
    print(f"\n{'='*60}")
    print(f"✓ SUCCESS - Translation saved!")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Translate subtitle files using Ollama',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  subtranslate "file.es.srt" --lang ja
  subtranslate "file.en.srt" --lang es --model gemma2:27b
  subtranslate "file.srt" --lang en --test 10
        """
    )
    
    parser.add_argument(
        'path',
        help='Path to subtitle file'
    )
    
    parser.add_argument(
        '--lang', '-l',
        required=True,
        help='Target language code (en, es, ja, fr, de, etc.)'
    )
    
    parser.add_argument(
        '--model', '-m',
        default=DEFAULT_MODEL,
        help=f'Ollama model to use (default: {DEFAULT_MODEL})'
    )
    
    parser.add_argument(
        '--test', '-t',
        type=int,
        metavar='N',
        help='Test mode: only translate first N entries'
    )
    
    parser.add_argument(
        '--no-debug',
        action='store_true',
        help='Disable debug messages'
    )
    
    args = parser.parse_args()
    
    global DEBUG
    DEBUG = not args.no_debug
    
    full_path = build_network_path(args.path)
    
    debug_print(f"Checking if file exists: {full_path}")
    if not os.path.exists(full_path):
        print(f"Error: File not found: {full_path}")
        return 1
    
    debug_print("File exists, proceeding with translation")
    
    try:
        translate_subtitle_file(full_path, args.lang, args.model, args.test)
        return 0
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"ERROR: {e}")
        print(f"{'='*60}\n")
        if DEBUG:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())