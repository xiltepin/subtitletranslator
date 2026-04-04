# Frontend — Angular UI

Angular 21 frontend for the Subtitle Translator AI.  
Runs as a Docker container on the LXC host (`<LXC_HOST_IP>`), exposed via Nginx Proxy Manager.

## Environment

| Item | Value |
|------|-------|
| Public URL | `<WEB_UI_URL>` |
| Port (host) | `4200` |
| Port (container) | `4200` |
| Backend API | `http://subtranslator-backend:5001` (internal Docker network) |

## Running (Docker — recommended)

```bash
cd /root/Tools/subtranslator/subtitle-translator-ai

# Start all services
docker compose up -d

# Rebuild after UI changes
docker compose up -d --build frontend

# Logs
docker compose logs -f frontend
```

## Development (local — without Docker)

```bash
cd subtitle-translator-front

# Install dependencies
npm install

# Start dev server (hot reload)
ng serve
# → http://localhost:4200
```

## Build

```bash
# Production build (not needed for Docker)
ng build
# Output in dist/
```

## Code Scaffolding

```bash
# Generate a new component
ng generate component component-name

# List all available schematics
ng generate --help
```

## Testing

```bash
# Unit tests (Vitest)
ng test

# End-to-end tests
ng e2e
```

## Key Files

| File/Folder | Purpose |
|-------------|---------|
| `src/app/` | Angular components and services |
| `src/environments/` | API endpoint configuration |
| `Dockerfile` | Container build (serves via `ng serve --host 0.0.0.0`) |
| `package.json` | NPM dependencies |

## Additional Resources

- [Angular CLI Documentation](https://angular.dev/tools/cli)
- [Angular 21 Release Notes](https://blog.angular.dev/)
