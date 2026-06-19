#!/bin/bash
set -e
cd /root/Tools/subtranslator

GITEA_URL="http://xiltepin:19770202Sae!@192.168.0.4:3000/xiltepin/subtitletranslator.git"

# Remove old remote if exists
git remote remove gitea 2>/dev/null || true

# Add Gitea remote with internal IP + credentials
git remote add gitea "$GITEA_URL"
echo "Remote added: $(git remote get-url gitea | sed 's|:.*@|:***@|')"

# Git push
echo "Pushing to Gitea..."
GIT_TERMINAL_PROMPT=0 git push -u gitea main 2>&1
echo "PUSH_EXIT=$?"
