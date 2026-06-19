#!/bin/bash
set -e
cd /root/Tools/subtranslator

echo "=== Git add all ==="
git add -A
git status --short

echo ""
echo "=== Commit ==="
git commit --allow-empty -F /root/Tools/subtranslator/commit_msg.txt 2>&1 || echo "Nothing to commit or already committed"

echo ""
echo "=== Push to gitea ==="
GITEA_URL="http://xiltepin:19770202Sae!@192.168.0.4:3000/xiltepin/subtitletranslator.git"
git remote remove gitea 2>/dev/null || true
git remote add gitea "$GITEA_URL"
GIT_TERMINAL_PROMPT=0 git push -u gitea main 2>&1
echo "PUSH_EXIT=$?"

echo "=== DONE ==="
echo "Repo: https://codigo.xiltepin.me/xiltepin/subtitletranslator"
