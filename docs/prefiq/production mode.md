✅ Perfect — everything’s in place for production.
Here’s what you should do to run **Prefiq in production mode**:

---

### 1. Set environment

In your `.env` or system environment, configure:

```bash
ENV=production
LOG_LEVEL=INFO
LOG_FORMAT=text     # or json if you’re shipping logs
LOG_COLOR=false     # avoid ANSI colors in production logs

DB_ENGINE=mariadb   # or postgres/sqlite
DB_MODE=async       # or sync if preferred
DB_HOST=your-prod-host
DB_PORT=3306        # 5432 for postgres
DB_USER=youruser
DB_PASS=yourpassword
DB_NAME=yourdbname
```

If you have multiple DBs (e.g. **DEV**, **ANALYTICS**), also set:

```bash
DEV_DB_ENGINE=postgres
DEV_DB_NAME=devdb
ANALYTICS_DB_ENGINE=postgres
ANALYTICS_DB_NAME=analyticsdb
```

---

### 2. Bootstrap the app

For production, you don’t run the raw `bootstrap.py`; you use the **CLI entrypoint**:

```bash
$ prefiq run migrate   # run migrations
$ prefiq run sanity    # quick checks
$ prefiq doctor boot   # validate providers + settings
$ prefiq doctor database --strict   # ensure DB connection works
```

---

### 3. Run server

If you want to expose APIs or services:

```bash
$ prefiq server start --host 0.0.0.0 --port 8080
```

(That mounts `bootstrap` + providers under uvicorn/gunicorn depending on your setup.)

---

### 4. Recommended production hardening

* **Logging**: ship logs to stdout/stderr only (already built-in). Forward them with Docker/k8s or journald.
* **Process manager**: run with `systemd`, `supervisord`, or Docker.
  Example with uvicorn:

  ```bash
  uvicorn prefiq.cli.core.server:app --host 0.0.0.0 --port 8080 --workers 4
  ```
* **DB pooling**: tune `DB_POOL_WARMUP` in `.env` to pre-warm async pools.
* **Secrets**: don’t hardcode `JWT_SECRET_KEY` in `.env` — use a secrets manager (Vault, AWS SSM, Docker secrets).

---

👉 Do you want me to prepare a **production-ready `.env.example` file** and a **systemd service unit** so you can just drop them in?
