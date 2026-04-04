# Subtitle Translator AI - Quick Reference Guide

## 🏗️ Environment

| Component | Value |
|-----------|-------|
| **Host** | `<LXC_HOST_IP>` — LXC container |
| **Media server (NAS)** | `<MEDIA_SERVER>` |
| **NAS mount point (host)** | `<NAS_MOUNT_HOST>` |
| **NAS mount point (container)** | `<NAS_MOUNT_CONTAINER>` (mapped via Docker volume) |
| **Ollama (GPU inference)** | `<OLLAMA_HOST>` |
| **Web UI** | `<WEB_UI_URL>` → `http://<LXC_HOST_IP>:4200` |
| **Backend API** | `http://<LXC_HOST_IP>:5001` |

---

## 🚀 Quick Start (Docker)

Everything runs via Docker Compose. No manual venv activation needed.

```bash
cd /root/Tools/subtranslator/subtitle-translator-ai

# Start all services
docker compose up -d

# Stop all services
docker compose down

# Rebuild and restart (after code changes)
docker compose up -d --build

# View logs
docker compose logs -f
docker compose logs -f backend
docker compose logs -f frontend
```

---

## 📁 Media Navigation (from host)

The Synology NAS share is mounted at `/mnt/synology` on the host machine.

```bash
# Check mount is live
ls /mnt/synology/

# Browse available content
ls /mnt/synology/Series/
ls /mnt/synology/Movies/

# Inside Docker the same share is visible as /mnt/media
# e.g. /mnt/synology/Series/Foo → /mnt/media/Series/Foo (inside container)
```

> **Note:** The NAS is mounted via `/etc/fstab` or `systemd.mount` on the LXC host. If the mount is lost after reboot, re-mount with:
> ```bash
> mount /mnt/synology
> ```

---

## 📝 CLI Translation Commands

The `subtranslate` command runs **inside the backend container** or directly via `translate.sh`.

### Basic Syntax
```bash
subtranslate "path/to/subtitle.srt" --lang TARGET_LANGUAGE [--model MODEL] [--context "description"] [--test N]
```

### Common Language Codes
| Code | Language |
|------|----------|
| `en` | English |
| `es` | Spanish |
| `ja` | Japanese |
| `fr` | French |
| `de` | German |
| `pt` | Portuguese |
| `zh` | Chinese |
| `ko` | Korean |

---

## 🎯 Using Context for Better Translations

**Context dramatically improves translation quality!** Always include a brief description of the content.

### Why Use Context?
- ✅ Better character name handling
- ✅ Appropriate tone (horror vs comedy vs drama)
- ✅ Accurate technical terminology
- ✅ Period-appropriate language
- ✅ Cultural reference adaptation

### Context Examples
```bash
# Horror series
subtranslate "file.en.srt" --lang ja --context "Horror series 1960s Maine clown"

# War movie
subtranslate "file.en.srt" --lang es --context "WWII Pacific theater US Marines historical"

# Sci-fi thriller
subtranslate "file.en.srt" --lang ja --context "Sci-fi thriller alien invasion modern Tokyo"

# Comedy series
subtranslate "file.en.srt" --lang es --context "Comedy series workplace humor modern office"

# Period drama
subtranslate "file.en.srt" --lang ja --context "Period drama 1800s Japan samurai feudal era"
```

---

## 🌍 English → Japanese Translation

### Default (Best Quality) — gemma3:12b
```bash
# With context (RECOMMENDED)
subtranslate "file.en.srt" --lang ja --context "Horror series 1960s Maine supernatural clown"

# Test first
subtranslate "file.en.srt" --lang ja --context "Horror 1960s" --test 5
```

**Speed**: ~2-3 seconds/entry | **Quality**: Excellent

### Fast — gemma2:9b
```bash
subtranslate "file.en.srt" --lang ja --model gemma2:9b --context "Action movie explosions"
```

**Speed**: ~1-2 seconds/entry | **Quality**: Good

---

## 🌍 English → Spanish Translation

### Default (Best Quality) — gemma3:12b
```bash
# With context (RECOMMENDED)
subtranslate "file.en.srt" --lang es --context "Horror series Stephen King 1960s Maine"

# Test first
subtranslate "file.en.srt" --lang es --context "Horror series" --test 5
```

### Fast — gemma2:9b
```bash
subtranslate "file.en.srt" --lang es --model gemma2:9b --context "Comedy workplace"
```

---

## 💡 Practical Examples (paths inside container)

### Example 1: IT Welcome to Derry (EN → JA)
```bash
cd "/mnt/media/Series/IT Welcome to Derry/Season1/IT.Welcome.to.Derry.S01E01.1080p.HEVC.x265-MeGusta/"

subtranslate "IT.Welcome.to.Derry.S01E01.1080p.HEVC.x265-MeGusta.en.srt" --lang ja \
  --context "Horror series 1960s Derry Maine, Stephen King IT prequel, Pennywise clown terrorizing town"

# Quick test first (recommended)
subtranslate "IT.Welcome.to.Derry.S01E01.1080p.HEVC.x265-MeGusta.en.srt" --lang ja \
  --context "Horror series 1960s Maine clown" --test 5
```

### Example 2: War Movie (EN → ES)
```bash
cd "/mnt/media/Movies/Saving Private Ryan/"

subtranslate "Saving.Private.Ryan.1998.en.srt" --lang es \
  --context "WWII D-Day Normandy invasion US Army military drama historical 1944"
```

### Example 3: Sci-Fi Series (EN → JA)
```bash
cd "/mnt/media/Series/The Expanse/"

subtranslate "The.Expanse.S01E01.en.srt" --lang ja \
  --context "Sci-fi space opera future solar system politics space warfare"
```

### Example 4: Comedy (EN → ES)
```bash
cd "/mnt/media/Series/The Office/"

subtranslate "The.Office.S01E01.en.srt" --lang es \
  --context "Comedy mockumentary office workplace humor awkward situations"
```

---

## 📊 Model Comparison

| Model | Speed | Quality | Best For |
|-------|-------|---------|----------|
| `gemma3:12b` | ⚡⚡ Medium | ⭐⭐⭐⭐ Excellent | **DEFAULT** — Best overall |
| `gemma2:9b` | ⚡⚡⚡ Fast | ⭐⭐⭐ Good | Quick translations |

---

## 📚 Context Writing Tips

### Good Context Examples
✅ `"Horror series 1960s Maine supernatural clown Stephen King"`  
✅ `"WWII Pacific theater US Marines historical accurate military"`  
✅ `"Sci-fi thriller AI rebellion cyberpunk dystopian future"`  
✅ `"Comedy workplace mockumentary awkward humor modern office"`  
✅ `"Period drama 1800s Victorian England aristocracy romance"`

### What to Include
- **Genre**: horror, comedy, drama, thriller, sci-fi
- **Setting**: time period, location
- **Tone**: serious, humorous, dark, lighthearted
- **Key elements**: character types, creator name

**Keep it concise** — 5-15 words is ideal.

---

## 🛠️ Useful Commands

### Check Docker Status
```bash
docker ps
docker compose logs -f backend
```

### Check Ollama Models (from host)
```bash
curl <OLLAMA_HOST>/api/tags
```

### Find Subtitle Files (from host)
```bash
# All SRT in Series
find /mnt/synology/Series/ -name "*.srt" -type f

# Only English SRTs
find /mnt/synology/Movies/ -name "*.en.srt"

# Only Spanish SRTs
find /mnt/synology/Series/ -name "*.es.srt"
```

---

## ⚙️ Optional Flags

| Flag | Description |
|------|-------------|
| `--lang CODE` | **Required.** Target language code |
| `--model NAME` | Override model (default: `gemma3:12b`) |
| `--context "text"` | Genre/setting description for better quality |
| `--test N` | Translate only first N entries (dry-run) |
| `--no-debug` | Suppress debug output |

```bash
# Test with context, specific model, no debug
subtranslate "file.srt" --lang es --model gemma2:9b \
  --context "war military WWII" --test 5 --no-debug
```

---

## 📁 Output Files

Translated files are saved in the **same directory** as the source, with the new language code:

```
Input:  IT.Welcome.to.Derry.S01E01.en.srt
Output: IT.Welcome.to.Derry.S01E01.ja.srt

Input:  movie.es.srt
Output: movie.en.srt
```

---

## 🔧 Troubleshooting

### Subtitles not loading in Web UI
```bash
# Verify synology mount is alive on the host
ls /mnt/synology/Series/
ls /mnt/synology/Movies/

# Check backend container sees the files
docker exec subtranslator-backend ls /mnt/media/Series/
```

### NAS Mount Lost After Reboot
```bash
# Re-mount
mount /mnt/synology

# Or check fstab / systemd mount unit
cat /etc/fstab | grep synology
```

### Model Not Available
```bash
# On the Ollama machine
ollama ls
ollama pull gemma3:12b
```

### Ollama Not Responding
```bash
# Test from LXC host
curl <OLLAMA_HOST>/api/tags
```

### Container Not Starting
```bash
cd /root/Tools/subtranslator/subtitle-translator-ai
docker compose down
docker compose up -d --build
docker compose logs -f
```

---

## 🎯 Recommended Workflow

1. **Verify mount**: `ls /mnt/synology/Series/`
2. **Open Web UI**: `https://subs.xiltepin.me`
3. **Select file** from the dropdown (scans `Series/` and `Movies/` automatically)
4. **Test with context**: use `--test 5` via CLI if testing manually
5. **Check quality**: Open the output `.srt` to verify
6. **Run full translation** via Web UI or CLI

---

## 🌟 Pro Tips

- **Always test first** with `--test 5` before translating full files
- **Always use context** for 30-50% better translation quality
- **Keep context concise** — 5-15 keywords is perfect
- **Use gemma3:12b** (default) for best quality
- **Use gemma2:9b** when speed matters more than quality
- **Check the output** after test mode before running full translation

---

*Script: `/root/Tools/subtranslator/subtitle-translator-ai/subtitle-translator-back/subtitle_translator.py`*  
*Default model: `gemma4:latest`*  
*Ollama host: `<OLLAMA_HOST>`*  
*Media host (NAS): `<MEDIA_SERVER>` — mounted at `<NAS_MOUNT_HOST>` on host, `<NAS_MOUNT_CONTAINER>` in container*  
*Updated: 2026-04-04*