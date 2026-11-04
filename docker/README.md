# Docker Infrastructure (`kb-back-adm`)

This directory houses the container orchestration files for the Kiribati Platform.

## Files
- **`compose.yml`**: Base Docker Compose definition (PostgreSQL DB, Adminer, Backend API, Frontend).
- **`compose.override.yml`**: Development overrides (source code volume sync, hot-reload, Mailcatcher, exposed debug ports).
- **`compose.traefik.yml`**: Traefik edge proxy with automatic Let's Encrypt SSL.

---

## How to Run

### Method 1: From the Project Root (Recommended)
```bash
# Start local development stack
docker compose --env-file .env -f docker/compose.yml -f docker/compose.override.yml up -d

# View live logs
docker compose --env-file .env -f docker/compose.yml -f docker/compose.override.yml logs -f backend

# Stop the stack
docker compose --env-file .env -f docker/compose.yml -f docker/compose.override.yml down
```

### Method 2: From the `docker/` Directory
```bash
cd docker

# Start stack
docker compose --env-file ../.env up -d

# Stop stack
docker compose --env-file ../.env down
```

