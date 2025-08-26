Here you go — dropped inline as requested:

# Prefiq HTTP Server — Usage Guide

This document explains how to run and manage the Prefiq FastAPI server, how it reads configuration from `.env`, and what
built-in endpoints and defaults you get out of the box.

---

## Quick start

```bash
# Development (binds to 127.0.0.1 by default)
prefiq server run
# or explicitly
prefiq server run dev

# Production-like (binds to 0.0.0.0 by default)
prefiq server run live
```

Output will include the full URL (host\:port) and runtime options (reload/workers).

---

## Environments & defaults

`prefiq server run <env>` accepts shorthand aliases:

| CLI arg | ENV value   | Default host |
|---------|-------------|--------------|
| dev     | development | 127.0.0.1    |
| live    | production  | 0.0.0.0      |
| stage   | staging     | 0.0.0.0      |
| test    | test        | 0.0.0.0      |

> You can still override the host via `.env` or the `--host` flag.

---

## Configuration via `.env`

These keys are read by `load_settings()` and used by the server CLI (CLI flags override `.env`):

```ini
# Networking
SERVER_HOST = 127.0.0.1     # dev default
SERVER_PORT = 5001

# Hot reload & workers
SERVER_RELOAD = false
SERVER_WORKERS = 1

# HTTPS (optional)
SERVER_HTTPS = false
SERVER_CERTFILE =
SERVER_KEYFILE =

# DB close behavior on process exit (sync engines only)
DB_CLOSE_ATEXIT = true
```

---

## CLI flags (override `.env`)

```bash
prefiq server run [dev|live|stage|test] \
  --host 127.0.0.1 \
  --port 5001 \
  --reload \
  --workers 4 \
  --https --certfile /path/cert.pem --keyfile /path/key.pem
```

Flags are also available on `start` and `restart`.

---

## Daemon mode (background)

# Start in background

```
prefiq server start dev
```

# Stop the background server

```
prefiq server stop
```

# Restart (stop if running, then start)
```
prefiq server restart live
```

Runtime files:

* PID: `<project_root>/.prefiq/server.pid`
* Logs: `<project_root>/.prefiq/server.log`

---

## Built-in endpoints

Available without any additional setup:

* `GET /` → `{"status": "running"}`
* `GET /healthz` → `{"ok": true|false}` (performs a light database connectivity check)
* `GET /favicon.ico` → serves `assets/images/favicon.svg` if present (204 otherwise)

CORS is enabled globally with permissive defaults (all origins, all methods, all headers).

---

## App factory & centralized shutdown

Both foreground and daemon use the same app factory:

* Factory: `prefiq.http.app:build_http_app` (used by uvicorn `--factory`)
* Preparation: attaches CORS, default routes, and a **FastAPI `shutdown` event** that closes DB pools and connections
  safely while the event loop is alive.

A small atexit fallback exists but only for **sync** engines, to avoid async scheduling during interpreter shutdown.

---

## Routing via Providers (Option A pattern)

Use the shared helper to mount routers inside provider `boot()`:

```python
from prefiq.http.routing import include_routes

# Cortex (root app, outside apps/)
include_routes("cortex.src.routes.web", prefix="/cortex", tags=["cortex:web"])
include_routes("cortex.src.routes.api", prefix="/api/cortex", tags=["cortex:api"])

# Devmeta (under apps/)
include_routes("apps.devmeta.src.routes.web", prefix="/devmeta", tags=["devmeta:web"])
include_routes("apps.devmeta.src.routes.api", prefix="/api/devmeta", tags=["devmeta:api"])
```

Each referenced module must export `router = APIRouter()`.

---

## Common troubleshooting

* **404 on /**
  Ensure you are running through the unified app factory (the CLI already does this).

* **`RuntimeError: cannot schedule new futures after interpreter shutdown` during exit**
  Centralized FastAPI shutdown closes connections; atexit avoids async work. If you still see this in custom code, don’t
  `asyncio.run()` anything from atexit.

* **No routes found**
  Check that Providers are discovered and their `boot()` calls `include_routes(...)`. Run:

```
prefiq provider list
```

```
prefiq doctor boot
```

---

## Command cheat sheet

```
prefiq server run           # dev (ENV=development)
```

```
prefiq server run dev
```

```
prefiq server run live      # ENV=production
```

# Background

```
prefiq server start dev
```

```
prefiq server stop
```

```
prefiq server restart live
```

# Flags

--host, --port, --reload, --workers, --https, --certfile, --keyfile

```
