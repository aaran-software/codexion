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



Project.py: domain rules only (validate name/code, status transitions).
IProject.py: contract for persistence (get_by_id, get_by_code, list, save, update, delete).
IProjectService.py: contract for use cases (create, get, list, update, delete).
ProjectService.py: enforce uniqueness/business policy; never do SQL here.
ProjectRepos.py: SQL and mapping (domain ↔ row) + tenant scope + pagination.
ProjectMemory.py: dict-backed collection for fast tests/dev.
ProjectProvider.py: Ensure the module is importable under an app listed.




contracts (interfaces)

prefiq/lowcode/contracts/IRepository.py — generic repo contract (get/list/save/update/delete).
prefiq/lowcode/contracts/IService.py — generic service contract (create/get/list/update/delete).
prefiq/lowcode/contracts/ITenantContext.py — current tenant + (optional) engine/schema hint.
prefiq/lowcode/contracts/IClock.py — time source.

runtime base classes

prefiq/foundation/EntityBase.py — base domain entity with small validation helpers.
prefiq/foundation/ServiceBase.py — implements common service ops; enforces basic policies.
prefiq/foundation/RepositorySqlBase.py — SQL CRUD with tenant scope, pagination, and simple mapping.
prefiq/foundation/RepositoryMemoryBase.py — in-memory CRUD for tests/dev.
prefiq/foundation/Mapper.py — row ⇄ domain mappers (overridable).
prefiq/foundation/Pagination.py — Page, PagedResult.
prefiq/foundation/Hooks.py — lifecycle hooks: before_create, after_create, before_update, after_update, etc.
prefiq/foundation/Policy.py — authorization/guard checks (row-level, field-level).
prefiq/foundation/Events.py — domain events + a tiny bus (for activity logs/notifications).

sql helpers

prefiq/lowcode/sql/Executor.py — thin wrapper over ConnectionManager (exec/query/scalar/tx).
prefiq/lowcode/sql/TenantScope.py — apply row-level, schema, or db-per-tenant filtering.

declaration (the “low-code” part)

prefiq/lowcode/declarative/ModelMeta.py — lets each domain model declare fields, indexes, defaults, validators, and status machine.
prefiq/lowcode/declarative/Scaffold.py — small utilities to generate controllers/routes/migrations from metadata (when you say so).

provider & cli

prefiq/lowcode/providers/LowcodeProvider.py — binds shared services (tenant, clock, sql executor).
prefiq/lowcode/cli/lowcode.py — commands to scaffold models/routes/migrations/docs from declarations.

prefiq/
  foundation/
    RepositoryBase.py
    ServiceBase.py
    ProviderBase.py
    SqlExecutor.py
    TenantScope.py
  contracts/
    IDomain.py
    IDomainService.py
    ITenantContext.py
    IClock.py


prefiq/foundation/Entity.py — base domain entity with small validation helpers.
prefiq/foundation/Services.py — implements common service ops; enforces basic policies.
prefiq/foundation/RepositoryQuery.py — SQL CRUD with tenant scope, pagination, and simple mapping.
prefiq/foundation/RepositoryMemory.py — in-memory CRUD for tests/dev.
prefiq/foundation/Mapper.py — row ⇄ domain mappers (overridable).
prefiq/foundation/Pagination.py — Page, PagedResult.
prefiq/foundation/Hooks.py — lifecycle hooks: before_create, after_create, before_update, after_update, etc.
prefiq/foundation/Policy.py — authorization/guard checks (row-level, field-level).
prefiq/foundation/Events.py — domain events + a tiny bus (for activity logs/notifications).

prefiq/contracts/IDomain.py
prefiq/contracts/IDomainService.py
prefiq/contracts/ITenantContext.py
prefiq/contracts/IClock.py



prefiq/
  foundation/
    Entity.py
    Services.py
    RepositoryQuery.py
    RepositoryMemory.py
    Mapper.py
    Pagination.py
    Hooks.py
    Policy.py
    Events.py
  contracts/
    IDomain.py
    IDomainService.py
    ITenantContext.py
    IClock.py
prefiq/
  foundation/
    Entity.py
    Services.py
    RepositoryQuery.py
    RepositoryMemory.py
    Mapper.py
    Pagination.py
    Hooks.py
    Policy.py
    Events.py
  contracts/
    IDomain.py
    IDomainService.py
    ITenantContext.py
    IClock.py

prefiq/
  foundation/
    Entity.py
    Services.py
    RepositoryQuery.py
    RepositoryMemory.py
    Mapper.py
    Pagination.py
    Hooks.py
    Policy.py
    Events.py
  contracts/
    IDomain.py
    IDomainService.py
    ITenantContext.py
    IClock.py
