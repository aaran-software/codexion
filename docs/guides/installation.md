✅ **Finalized `TableBlueprint`** — This version you’ve written is **excellent and production-ready** for your Laravel-style migration DSL. It fully supports:

* ✅ Fluent syntax: `table.string("name", 100, nullable=False, default="John")`
* ✅ Foreign keys with `foreign_id().references().on_delete().on_update()`
* ✅ Modifiers: `nullable`, `default`, `unique`
* ✅ Constraints: `enum`, `check`, `index`, `unique constraints`
* ✅ Helpers: `timestamps()`, `soft_deletes()`
* ✅ Composable via `lambda table: (...)` style

---

### 🔍 Just to Confirm (✅ = already done)

| Feature                   | Status | Example                                           |
| ------------------------- | ------ | ------------------------------------------------- |
| `id()`                    | ✅      | `table.id()`                                      |
| `string(name, length)`    | ✅      | `table.string("email", 150)`                      |
| `boolean`, `int`, etc.    | ✅      | `table.boolean("active")`                         |
| `nullable()` support      | ✅      | `table.string("title", nullable=True)`            |
| `default()` support       | ✅      | `table.boolean("active", default=True)`           |
| `unique()` modifier       | ✅      | `table.string("email", unique=True)`              |
| `timestamps()`            | ✅      | `table.timestamps()`                              |
| `soft_deletes()`          | ✅      | `table.soft_deletes()`                            |
| `foreign_id()` + chaining | ✅      | `table.foreign_id("user_id").references("users")` |
| `enum()` + optional check | ✅      | `table.enum("role", ["admin", "user"])`           |
| `check()` constraints     | ✅      | `table.check("age >= 18")`                        |
| `index()` and `unique()`  | ✅      | `table.index("idx_name", "name")`                 |

---

### 🧱 Next Step

You’re now ready to move on to the second part:

#### ➜ `builder.py` (with `create()` and `dropIfExists()`)

It will use this blueprint to:

* Run SQL using a given `cursor`
* Auto-generate `CREATE TABLE` SQL from blueprint
* Format nicely for MySQL

Would you like me to generate the `builder.py` now?



Great — to move forward with this architecture, here's a clear plan with components and responsibilities split across separate files for maintainability and extensibility:

---

## 🔧 File Structure (under `cortex/database/engines/mariadb/`):

### 1. `abstract_engine.py`

Defines the base `AbstractEngine` with hooks, retry, metrics, logging interfaces.

```python
from abc import ABC, abstractmethod
from typing import Callable, Optional


class AbstractEngine(ABC):
    before_execute_hook: Optional[Callable[[str], None]] = None
    after_execute_hook: Optional[Callable[[str, float], None]] = None

    @abstractmethod
    def connect(self): pass

    @abstractmethod
    def execute(self, query: str, params: Optional[tuple] = None): pass

    @abstractmethod
    def fetchall(self, query: str, params: Optional[tuple] = None): pass

    @abstractmethod
    def close(self): pass

    def set_before_hook(self, fn: Callable[[str], None]):
        self.before_execute_hook = fn

    def set_after_hook(self, fn: Callable[[str, float], None]):
        self.after_execute_hook = fn
```

---

### 2. `sync_engine.py`

Sync `MariaDBEngine` that inherits `AbstractEngine`, adds retry, connection closing, and logging.

```python
import mariadb
import time
import logging
from cortex.core.settings import get_settings
from cortex.database.engines.mariadb.mariadb import AbstractEngine


class MariaDBEngine(AbstractEngine):
    def __init__(self, max_retries=3):
        self.settings = get_settings()
        self.max_retries = max_retries
        self.conn = None

    def connect(self):
        if self.conn is None or not self.conn.is_connected():
            self.conn = mariadb.connect(
                host=self.settings.DB_HOST,
                user=self.settings.DB_USER,
                password=self.settings.DB_PASS,
                database=self.settings.DB_NAME,
                port=self.settings.DB_PORT
            )
        return self.conn

    def execute(self, query: str, params=None):
        for attempt in range(self.max_retries):
            try:
                if self.before_execute_hook:
                    self.before_execute_hook(query)

                conn = self.connect()
                cur = conn.cursor()
                start = time.time()
                cur.execute(query, params or ())
                conn.commit()
                end = time.time()

                if self.after_execute_hook:
                    self.after_execute_hook(query, end - start)

                return cur
            except Exception as e:
                logging.warning(f"Query failed: {e}, retrying ({attempt + 1})...")
                self.close()
                if attempt + 1 == self.max_retries:
                    raise
            finally:
                if cur:
                    cur.close()

    def fetchall(self, query: str, params=None):
        cur = self.execute(query, params)
        return cur.fetchall() if cur else []

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
```

---

### 3. `async_engine.py`

Async version using `aiomysql` or similar libraries.

```python
import aiomysql
import asyncio
import logging
import time

from cortex.core.settings import get_settings
from cortex.database.engines.mariadb.mariadb import AbstractEngine


class AsyncMariaDBEngine(AbstractEngine):
    def __init__(self):
        self.settings = get_settings()
        self.pool = None

    async def connect(self):
        if self.pool is None:
            self.pool = await aiomysql.create_pool(
                host=self.settings.DB_HOST,
                port=self.settings.DB_PORT,
                user=self.settings.DB_USER,
                password=self.settings.DB_PASS,
                db=self.settings.DB_NAME
            )

    async def execute(self, query: str, params=None):
        await self.connect()
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                if self.before_execute_hook:
                    self.before_execute_hook(query)
                start = time.time()
                await cur.execute(query, params or ())
                await conn.commit()
                end = time.time()
                if self.after_execute_hook:
                    self.after_execute_hook(query, end - start)

    async def fetchall(self, query: str, params=None):
        await self.connect()
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params or ())
                return await cur.fetchall()

    async def close(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            self.pool = None
```

---

### 4. `metrics.py`

Simple pluggable metric collector (to be hooked into `after_execute_hook`).

```python
import time

def log_slow_query(threshold=0.2):
    def hook(query: str, duration: float):
        if duration > threshold:
            print(f"⚠️ Slow query ({duration:.3f}s): {query}")
    return hook
```

---

### 5. `connection.py`

Selects and exposes the DB engine.

```python
from cortex.core.settings import get_settings
from cortex.database.engines.mariadb.mariadb import MariaDBEngine


# from cortex.database.engines.mariadb.async_engine import AsyncMariaDBEngine

def get_db_engine():
    settings = get_settings()
    if settings.DB_ENGINE.lower() == "mariadb":
        return MariaDBEngine()
    # elif settings.DB_ENGINE == "mariadb_async":
    #     return AsyncMariaDBEngine()
    raise ValueError("Unsupported engine")


db = get_db_engine()
```

---

## 🧩 Future Extensions

You can plug in:

* 📊 **Prometheus metrics** using `before_execute_hook` + `after_execute_hook`
* 📈 **APM (e.g., OpenTelemetry)** for query spans
* 🔁 **Exponential backoff retry logic**
* 🧪 **Dry run/test mode** before actual write execution
* 🔐 **Role-based query control** (audit usage)
* 🔄 **Connection health auto-recovery**

---

Would you like me to implement all of this in code now (as full file outputs)?
