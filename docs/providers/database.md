Perfect. Let’s draft the **DatabaseProvider** properly — as a design document + code skeleton — so it fits into your existing `/core` provider system.

---

# 🗄️ `DatabaseProvider` – Design Document

## 📌 Purpose

The **DatabaseProvider** manages database connections for the ERP.
It abstracts DB engines (Postgres, MySQL, SQLite, Oracle, etc.), exposes a consistent interface, and binds connection/session objects into the global `Application` container for other providers to use.

---

## 🎯 Goals

* **Environment-aware configuration** → values pulled from `settings` provider.
* **Pluggable engines** → Postgres, MySQL, SQLite, etc. (future: NoSQL).
* **Unified access** → always resolve via `app.resolve("db")`.
* **Lifecycle management** → connection pool setup at `register()`, cleanup at `boot()` or `shutdown()`.
* **Extensible** → future support for ORM (SQLAlchemy) or raw drivers.

---

## 📁 Location

```
cortex/core/providers/database_provider.py
```

---

## 🧩 Dependencies

* Relies on **SettingsProvider** (`app.resolve("settings")`) for DB config.
* Config namespace:

```yaml
database:
  engine: postgres
  url: postgresql://user:pass@localhost/db
  pool_size: 10
```

---

## ⚙️ Lifecycle

* **register()** → parse settings, init DB engine/pool, bind connection handle.
* **boot()** → verify connectivity, log status.
* **shutdown() (future)** → gracefully close connections.

---

## 🚦 Skeleton Code

```python
# cortex/core/providers/database_provider.py

from typing import Any, Dict, Optional
from cortex.core.contracts.base_provider import BaseProvider, register_provider


@register_provider
class DatabaseProvider(BaseProvider):
    """
    Database Provider
    -----------------
    Manages database connections using settings provided by SettingsProvider.
    """

    schema_namespace = "database"   # (optional future validation)

    def __init__(self, app) -> None:
        super().__init__(app)
        self.config: Dict[str, Any] = {}
        self.connection: Optional[Any] = None  # could be SQLAlchemy engine, psycopg conn, etc.

    def register(self) -> None:
        settings = self.app.resolve("settings") or {}
        db_conf = settings.get("database", {})

        # store config for use
        self.config = {
            "engine": db_conf.get("engine", "sqlite"),
            "url": db_conf.get("url", "sqlite:///app.db"),
            "pool_size": db_conf.get("pool_size", 5),
        }

        # TODO: Initialize engine/connection pool
        # Example placeholder:
        self.connection = f"[DB-CONNECTION] {self.config['engine']} @ {self.config['url']}"

        # bind into app container
        self.app.bind("db", self.connection)

    def boot(self) -> None:
        # TODO: actually verify connectivity
        print(f"[DatabaseProvider] Booted with engine={self.config['engine']} url={self.config['url']}")
```

---

## 📋 TODOs

* [x] Implement real DB driver handling (e.g., SQLAlchemy engine or psycopg for Postgres).
* [ ] Add health check in `boot()` (ping DB).
* [ ] Add `shutdown()` to close pools.
* [ ] Support multiple DBs (namespaced: `"db.main"`, `"db.analytics"`).
* [ ] Add observability hooks (query logging, tracing).
* [ ] Add retry/backoff for transient DB errors.

---

## ✅ Example Config

`settings.dev.yaml`

```yaml
database:
  engine: postgres
  url: postgresql://user:pass@localhost/devdb
  pool_size: 10
```

`settings.prod.yaml`

```yaml
database:
  engine: mysql
  url: mysql://user:pass@prod-db.company.com/proddb
  pool_size: 50
```

---

With this, **DatabaseProvider** is drafted & aligned with your core system.
It’s minimal now (just a skeleton), but structured to grow into a full enterprise DB layer.

---

👉 Do you want me to extend this skeleton with **SQLAlchemy support** right away (so you get a real engine/session object), or keep it **abstract** for now until you choose a DB stack?
