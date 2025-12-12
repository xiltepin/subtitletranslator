# Subtitle Translator - Quick Reference Guide

## 🚀 Quick Start

### 1. Mount the Network Share (if not already mounted)
```bash
# Check if already mounted
ls /mnt/media/

# If empty or error, mount the share:
sudo mount -t drvfs '\\192.168.0.2\Media' /mnt/media
```

### 2. Navigate to Media Path
```bash
# Go to the media root
cd /mnt/media/

# Navigate to a specific series
cd /mnt/media/Series/

# Navigate to a specific movie
cd /mnt/media/Movies/

# Example: Navigate to IT Welcome to Derry
cd "/mnt/media/Series/IT Welcome to Derry/Season1/"
```

**Tip**: Use `Tab` key for auto-completion when typing paths with spaces!

---

## 📝 Translation Commands

### Basic Syntax
```bash
subtranslate "path/to/subtitle.srt" --lang TARGET_LANGUAGE [--model MODEL_NAME] [--test N]
```

### Common Language Codes
- `en` = English
- `es` = Spanish  
- `ja` = Japanese
- `fr` = French
- `de` = German
- `pt` = Portuguese
- `zh` = Chinese
- `ko` = Korean

---

## 🌍 English to Japanese Translation

### Fast Translation (2-3 seconds per subtitle)
```bash
# Using qwen2.5:7b - Good quality, fast speed
subtranslate "file.en.srt" --lang ja --model qwen2.5:7b

# Test with first 5 entries
subtranslate "file.en.srt" --lang ja --model qwen2.5:7b --test 5
```

**Best for**: Quick translations, long subtitle files  
**Speed**: ~2-3 seconds per entry  
**Quality**: Good

### High Accuracy Translation (6-7 seconds per subtitle)
```bash
# Using qwen2.5:14b - Excellent quality for Asian languages
subtranslate "file.en.srt" --lang ja --model qwen2.5:14b

# Or use default (qwen2.5:14b is now default)
subtranslate "file.en.srt" --lang ja

# Test with first 5 entries
subtranslate "file.en.srt" --lang ja --test 5
```

**Best for**: Best Japanese translation quality  
**Speed**: ~6-7 seconds per entry  
**Quality**: Excellent

### Maximum Quality (Slower)
```bash
# Using qwen2.5:32b - Best quality, slower
subtranslate "file.en.srt" --lang ja --model qwen2.5:32b

# Test first
subtranslate "file.en.srt" --lang ja --model qwen2.5:32b --test 5
```

**Best for**: Professional translations, short files  
**Speed**: ~10-15 seconds per entry  
**Quality**: Best

---

## 🌍 English to Spanish Translation

### Fast Translation (1-2 seconds per subtitle)
```bash
# Using gemma2:9b - Fast and good for European languages
subtranslate "file.en.srt" --lang es --model gemma2:9b

# Test with first 5 entries
subtranslate "file.en.srt" --lang es --model gemma2:9b --test 5
```

**Best for**: Quick translations, everyday use  
**Speed**: ~1-2 seconds per entry  
**Quality**: Good

### High Accuracy Translation (3-5 seconds per subtitle)
```bash
# Using gemma2:27b - Excellent quality for European languages
subtranslate "file.en.srt" --lang es --model gemma2:27b

# Test with first 5 entries
subtranslate "file.en.srt" --lang es --model gemma2:27b --test 5
```

**Best for**: Best Spanish translation quality  
**Speed**: ~3-5 seconds per entry  
**Quality**: Excellent

### Alternative Option
```bash
# Using qwen2.5:14b - Also works well for Spanish
subtranslate "file.en.srt" --lang es --model qwen2.5:14b
```

---

## 💡 Practical Examples

### Example 1: Translate IT Welcome to Derry (Spanish → Japanese)
```bash
# Navigate to the episode folder
cd "/mnt/media/Series/IT Welcome to Derry/Season1/IT.Welcome.to.Derry.S01E01.1080p.HEVC.x265-MeGusta/"

# Fast translation
subtranslate "IT.Welcome.to.Derry.S01E01.1080p.HEVC.x265-MeGusta.es.sdh.srt" --lang ja --model qwen2.5:7b

# High quality translation
subtranslate "IT.Welcome.to.Derry.S01E01.1080p.HEVC.x265-MeGusta.es.sdh.srt" --lang ja
```

### Example 2: Translate Movie (English → Spanish)
```bash
# Navigate to movie folder
cd "/mnt/media/Movies/Alita Battle Angel/"

# Fast translation
subtranslate "Alita.Battle.Angel.2019.en.srt" --lang es --model gemma2:9b

# High quality translation
subtranslate "Alita.Battle.Angel.2019.en.srt" --lang es --model gemma2:27b
```

### Example 3: Test Before Full Translation
```bash
# Always test with first 5-10 entries before running full translation
subtranslate "$(pwd)/subtitle.en.srt" --lang ja --test 5

# If satisfied, run full translation
subtranslate "$(pwd)/subtitle.en.srt" --lang ja
```

---

## 📊 Model Comparison Table

| Model | Languages | Speed | Quality | Best For |
|-------|-----------|-------|---------|----------|
| `qwen2.5:7b` | Asian (JA/ZH/KO) | ⚡⚡⚡ Fast | ⭐⭐⭐ Good | Quick Japanese/Chinese/Korean |
| `qwen2.5:14b` | Asian (JA/ZH/KO) | ⚡⚡ Medium | ⭐⭐⭐⭐ Excellent | Best Japanese/Chinese/Korean |
| `qwen2.5:32b` | Asian (JA/ZH/KO) | ⚡ Slow | ⭐⭐⭐⭐⭐ Best | Professional Asian languages |
| `gemma2:9b` | European (ES/FR/DE) | ⚡⚡⚡ Fast | ⭐⭐⭐ Good | Quick Spanish/French/German |
| `gemma2:27b` | European (ES/FR/DE) | ⚡⚡ Medium | ⭐⭐⭐⭐ Excellent | Best Spanish/French/German |

---

## 🛠️ Useful Commands

### Check Available Models
```bash
curl http://192.168.0.6:11434/api/tags
```

### Install New Models
```bash
# Install a fast model
ollama pull qwen2.5:7b

# Install a high-quality model
ollama pull gemma2:27b

# Install maximum quality model
ollama pull qwen2.5:32b
```

### Navigate and Find Subtitles
```bash
# List all series
ls /mnt/media/Series/

# Find all Spanish subtitles
find /mnt/media/Series/ -name "*.es.srt"

# Find all English subtitles
find /mnt/media/Movies/ -name "*.en.srt"
```

### Using $(pwd) Shortcut
```bash
# Instead of typing the full path
subtranslate "/mnt/media/Series/Long/Path/To/File/subtitle.srt" --lang ja

# Use $(pwd) when you're in the same folder
cd "/mnt/media/Series/Long/Path/To/File/"
subtranslate "$(pwd)/subtitle.srt" --lang ja
```

---

## ⚙️ Optional Flags

### Test Mode
```bash
# Translate only first 10 entries to test quality/speed
subtranslate "file.srt" --lang ja --test 10
```

### Disable Debug Messages
```bash
# Cleaner output without debug info
subtranslate "file.srt" --lang ja --no-debug
```

### Combine Flags
```bash
# Test with specific model and no debug messages
subtranslate "file.srt" --lang es --model gemma2:9b --test 5 --no-debug
```

---

## 📝 Output Files

Translated files are saved in the **same directory** with the new language code:

```
Input:  IT.Welcome.to.Derry.S01E01.es.sdh.srt
Output: IT.Welcome.to.Derry.S01E01.ja.srt

Input:  movie.en.srt
Output: movie.es.srt
```

---

## 🔧 Troubleshooting

### Mount is Lost After Reboot
```bash
# Remount the share
sudo mount -t drvfs '\\192.168.0.2\Media' /mnt/media
```

### File Not Found Error
```bash
# Check if file exists
ls -la "path/to/file.srt"

# Make sure you're using the correct path with spaces in quotes
subtranslate "/mnt/media/Series/Name With Spaces/file.srt" --lang ja
```

### Model Not Available
```bash
# Pull the model first
ollama pull qwen2.5:14b

# Check available models
curl http://192.168.0.6:11434/api/tags
```

### Ollama Not Responding
```bash
# Check if Ollama is running on 192.168.0.6
curl http://192.168.0.6:11434/api/tags

# If not working, check Ollama service on the host machine
```

---

## 📌 Quick Reference Summary

```bash
# Mount media share
sudo mount -t drvfs '\\192.168.0.2\Media' /mnt/media

# Navigate to media
cd /mnt/media/Series/  # or /mnt/media/Movies/

# Fast English → Japanese
subtranslate "file.en.srt" --lang ja --model qwen2.5:7b

# Best English → Japanese  
subtranslate "file.en.srt" --lang ja

# Fast English → Spanish
subtranslate "file.en.srt" --lang es --model gemma2:9b

# Best English → Spanish
subtranslate "file.en.srt" --lang es --model gemma2:27b

# Always test first!
subtranslate "file.srt" --lang TARGET --test 5
```

---

## 🎯 Recommended Workflow

1. **Mount the share**: `sudo mount -t drvfs '\\192.168.0.2\Media' /mnt/media`
2. **Navigate to folder**: `cd /mnt/media/Series/ShowName/`
3. **Test translation**: `subtranslate "file.srt" --lang TARGET --test 5`
4. **Check quality**: Open the output file to verify
5. **Run full translation**: `subtranslate "file.srt" --lang TARGET`
6. **Repeat for other files**: Use the same model if quality is good

---

*Script location: `/home/xiltepin/tools/subtranslator/subtitle_translator.py`*  
*Ollama host: `192.168.0.6:11434`*  
*Media server: `\\192.168.0.2\Media`*
subtranslate "filename" --lang ja --model gemma2:27b