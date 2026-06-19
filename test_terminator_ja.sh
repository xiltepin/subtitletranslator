#!/bin/bash
# Quick test script: translate first 50 lines of The Terminator (1984) to Japanese
# Uses gemma4:e4b via Ollama at 192.168.0.6

VENV="/root/Tools/subtranslator/.venv"
SCRIPT="/root/Tools/subtranslator/subtitle_translator.py"
SRT="/mnt/synology/Movies/The.Terminator.1984.REMASTERED.1080p.BluRay.x265-LAMA/Subs/English.srt"

echo "=== Terminator 1984 - Japanese Translation Test ==="
echo "Model: gemma4:e4b"
echo "Lines: 50"
echo ""

source "$VENV/bin/activate" 2>/dev/null || true

python3 "$SCRIPT" \
    "$SRT" \
    --lang ja \
    --model "gemma4:e4b" \
    --test 50 \
    --context "The Terminator 1984 sci-fi action film, Arnold Schwarzenegger robot assassin from future, Sarah Connor, Kyle Reese, dystopian future war against machines" \
    2>&1

echo ""
echo "=== Test complete! ==="
echo "Check output file next to the .srt source."
