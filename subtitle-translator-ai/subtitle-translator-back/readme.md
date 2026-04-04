# Backend — Flask API

Python 3.11 / Flask backend that serves the subtitle translation API.  
Runs as a Docker container on the LXC host (`<LXC_HOST_IP>`).

## Environment

| Item | Value |
|------|-------|
| Port (host) | `5001` |
| Port (container) | `5001` |
| Media mount (host) | `<NAS_MOUNT_HOST>` |
| Media mount (container) | `<NAS_MOUNT_CONTAINER>` |
| Ollama | `<OLLAMA_HOST>` (set via `OLLAMA_HOST` env var) |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/files` | List all `.srt` files under `Series/` and `Movies/` |
| GET | `/api/models` | List available Ollama models |
| GET | `/api/translate` | Stream translation progress (SSE) |
| GET | `/api/readme` | Return this README as JSON |

## Running (Docker — recommended)

```bash
cd /root/Tools/subtranslator/subtitle-translator-ai

# Start
docker compose up -d

# Rebuild after code changes
docker compose up -d --build backend

# Logs
docker compose logs -f backend

# Shell into container
docker exec -it subtranslator-backend bash
```

## Running Locally (development only)

```bash
cd /root/Tools/subtranslator/subtitle-translator-ai

# Create venv if not exists
python3 -m venv .venv
source .venv/bin/activate
pip install -r subtitle-translator-back/requirements.txt

cd subtitle-translator-back
python3 app.py
```

## Key Files

| File | Purpose |
|------|---------|
| `app.py` | Flask application — all API routes |
| `subtitle_translator.py` | Core translation logic (also CLI) |
| `translate.sh` | Shell wrapper called by the API for streaming |
| `Dockerfile` | Container build definition |

## Configuration

All configuration is handled via environment variables in `docker-compose.yml` or `.env`:

```yaml
environment:
  - OLLAMA_HOST=${OLLAMA_HOST}
```

The media path inside the container is mapped from `<NAS_MOUNT_HOST>` on the host to `<NAS_MOUNT_CONTAINER>`.
