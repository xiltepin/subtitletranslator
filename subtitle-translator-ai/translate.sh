#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source ~/subtitle-env/bin/activate 2>/dev/null || true
python "$SCRIPT_DIR/subtitle_translator.py" "$@"
