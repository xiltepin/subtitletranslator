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
subtranslate "path/to/subtitle.srt" --lang TARGET_LANGUAGE [--model MODEL_NAME] [--context "description"] [--test N]
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

## 🌍 English to Japanese Translation

### Default (Best Quality) - gemma2:27b
```bash
# With context (RECOMMENDED)
subtranslate "file.en.srt" --lang ja --context "Horror series 1960s Maine supernatural clown"

# Without context
subtranslate "file.en.srt" --lang ja

# Test first
subtranslate "file.en.srt" --lang ja --context "Horror 1960s" --test 5
```

**Model**: `gemma2:27b` (default)  
**Speed**: ~2-3 seconds per entry  
**Quality**: Excellent

### Fast Translation - gemma2:9b
```bash
# With context
subtranslate "file.en.srt" --lang ja --model gemma2:9b --context "Action movie explosions"

# Test mode
subtranslate "file.en.srt" --lang ja --model gemma2:9b --test 5
```

**Speed**: ~1-2 seconds per entry  
**Quality**: Good

---

## 🌍 English to Spanish Translation

### Default (Best Quality) - gemma2:27b
```bash
# With context (RECOMMENDED)
subtranslate "file.en.srt" --lang es --context "Horror series Stephen King 1960s Maine"

# Without context
subtranslate "file.en.srt" --lang es

# Test first
subtranslate "file.en.srt" --lang es --context "Horror series" --test 5
```

**Model**: `gemma2:27b` (default)  
**Speed**: ~2-3 seconds per entry  
**Quality**: Excellent

### Fast Translation - gemma2:9b
```bash
# With context
subtranslate "file.en.srt" --lang es --model gemma2:9b --context "Comedy workplace"

# Test mode
subtranslate "file.en.srt" --lang es --model gemma2:9b --test 5
```

**Speed**: ~1-2 seconds per entry  
**Quality**: Good

---

## 💡 Practical Examples

### Example 1: IT Welcome to Derry (English → Japanese)
```bash
# Navigate to episode folder
cd "/mnt/media/Series/IT Welcome to Derry/Season1/IT.Welcome.to.Derry.S01E01.1080p.HEVC.x265-MeGusta/"

# With context for best quality
subtranslate "IT.Welcome.to.Derry.S01E01.1080p.HEVC.x265-MeGusta.en.srt" --lang ja \
  --context "Horror series 1960s Derry Maine, Stephen King IT prequel, Pennywise clown terrorizing town"

# Quick test first (recommended)
subtranslate "IT.Welcome.to.Derry.S01E01.1080p.HEVC.x265-MeGusta.en.srt" --lang ja \
  --context "Horror series 1960s Maine clown" --test 5
```

### Example 2: War Movie (English → Spanish)
```bash
cd "/mnt/media/Movies/Saving Private Ryan/"

# With military context
subtranslate "Saving.Private.Ryan.1998.en.srt" --lang es \
  --context "WWII D-Day Normandy invasion US Army military drama historical 1944"

# Test first
subtranslate "Saving.Private.Ryan.1998.en.srt" --lang es \
  --context "WWII military historical" --test 5
```

### Example 3: Sci-Fi Series (English → Japanese)
```bash
cd "/mnt/media/Series/The Expanse/"

# With sci-fi context
subtranslate "The.Expanse.S01E01.en.srt" --lang ja \
  --context "Sci-fi space opera future solar system politics space warfare"
```

### Example 4: Comedy (English → Spanish)
```bash
cd "/mnt/media/Series/The Office/"

# With comedy workplace context
subtranslate "The.Office.S01E01.en.srt" --lang es \
  --context "Comedy mockumentary office workplace humor awkward situations"
```

---

## 📚 Context Writing Tips

### Good Context Examples:
✅ `"Horror series 1960s Maine supernatural clown Stephen King"`  
✅ `"WWII Pacific theater US Marines historical accurate military"`  
✅ `"Sci-fi thriller AI rebellion cyberpunk dystopian future"`  
✅ `"Comedy workplace mockumentary awkward humor modern office"`  
✅ `"Period drama 1800s Victorian England aristocracy romance"`

### What to Include:
- **Genre**: horror, comedy, drama, thriller, sci-fi
- **Setting**: time period, location
- **Themes**: supernatural, military, workplace, romance
- **Tone**: serious, humorous, dark, lighthearted
- **Key elements**: character types, situations

### Keep It Concise:
- 5-15 words is ideal
- Focus on key distinctive elements
- Use keywords, not full sentences

---

## 📊 Model Comparison Table

| Model | Languages | Speed | Quality | Best For |
|-------|-----------|-------|---------|----------|
| `gemma2:27b` | All | ⚡⚡ Medium | ⭐⭐⭐⭐ Excellent | **DEFAULT** - Best overall |
| `gemma2:9b` | All | ⚡⚡⚡ Fast | ⭐⭐⭐ Good | Quick translations |
| `gemma3:12b` | All | ⚡⚡ Medium | ⭐⭐⭐⭐ Excellent | Alternative quality option |
| `gpt-oss:20b` | All | ⚡ Slow | ⭐⭐⭐ Good | Not recommended |

---

## 🛠️ Useful Commands

### Check Available Models
```bash
ollama ls
```

### Install New Models
```bash
# Install fast model
ollama pull gemma2:9b

# Install high-quality model (already installed)
ollama pull gemma2:27b

# Install alternative
ollama pull gemma3:12b
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
subtranslate "subtitle.srt" --lang ja --context "genre description"
```

---

## ⚙️ Optional Flags

### Test Mode (ALWAYS RECOMMENDED)
```bash
# Test first 5 entries before full translation
subtranslate "file.srt" --lang ja --context "horror 1960s" --test 5

# Test first 10 entries
subtranslate "file.srt" --lang es --test 10
```

### Disable Debug Messages
```bash
# Cleaner output without debug info
subtranslate "file.srt" --lang ja --no-debug
```

### Specify Model
```bash
# Use faster model
subtranslate "file.srt" --lang es --model gemma2:9b --context "comedy"

# Use default (gemma2:27b)
subtranslate "file.srt" --lang ja --context "sci-fi"
```

### Combine Flags
```bash
# Test with context, specific model, no debug
subtranslate "file.srt" --lang es --model gemma2:9b \
  --context "war military WWII" --test 5 --no-debug
```

---

## 📁 Output Files

Translated files are saved in the **same directory** with the new language code:
```
Input:  IT.Welcome.to.Derry.S01E01.en.srt
Output: IT.Welcome.to.Derry.S01E01.ja.srt

Input:  movie.es.srt
Output: movie.en.srt
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
# Check available models
ollama ls

# Pull missing model
ollama pull gemma2:27b
```

### Ollama Not Responding
```bash
# Check if Ollama is running
curl http://192.168.0.6:11434/api/tags

# If not working, check Ollama service on 192.168.0.6
```

---

## 📌 Quick Reference Summary
```bash
# Mount media share
sudo mount -t drvfs '\\192.168.0.2\Media' /mnt/media

# Navigate to media
cd /mnt/media/Series/  # or /mnt/media/Movies/

# RECOMMENDED: Always use context for best quality
subtranslate "file.en.srt" --lang ja --context "horror 1960s Maine clown"
subtranslate "file.en.srt" --lang es --context "war WWII military"

# Test first (5-10 entries)
subtranslate "file.srt" --lang ja --context "description" --test 5

# Fast translation (less accurate)
subtranslate "file.en.srt" --lang es --model gemma2:9b
```

---

## 🎯 Recommended Workflow

1. **Mount the share**: `sudo mount -t drvfs '\\192.168.0.2\Media' /mnt/media`
2. **Navigate to folder**: `cd /mnt/media/Series/ShowName/`
3. **Test with context**: `subtranslate "file.srt" --lang ja --context "genre time period" --test 5`
4. **Check quality**: Open the output file to verify
5. **Run full translation**: `subtranslate "file.srt" --lang ja --context "same context"`
6. **Repeat for other files**: Use the same context and model if quality is good

---

## 🌟 Pro Tips

- **Always test first** with `--test 5` before translating full files
- **Always use context** for 30-50% better translation quality
- **Keep context concise** - 5-15 keywords is perfect
- **Use gemma2:27b** (default) for best quality
- **Use gemma2:9b** when speed matters more than quality
- **Check the output** after test mode before running full translation

---

*Script location: `/home/xiltepin/tools/subtranslator/subtitle_translator.py`*  
*Default model: `gemma2:27b`*  
*Ollama host: `192.168.0.6:11434`*  
*Media server: `\\192.168.0.2\Media`*