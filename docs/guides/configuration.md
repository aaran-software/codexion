Here’s a **clean and modular recap** of your custom **MariaDB database engine** repository structure with **async support**, **pooling**, **retry logic**, **hooks**, **logging**, and **metrics**, split into organized files:

---

### 📁 `core/database/mariadb/`

Modular async MariaDB engine with full lifecycle support.

```
core/
└── database/
    └── mariadb/
        ├── sync_engine.py           # ← SyncMariaDBEngine
        ├── async_engine.py         # ← AsyncMariaDBEngine
        ├── pool.py
        ├── retry.py
        ├── hooks.py
        ├── logger.py
        ├── metrics.py
        └── health.py
        
    ├── abstract_engine.py
```

---

## 🔍 **File-wise Breakdown**

### ✅ `abstract.py`

Defines the base `AbstractEngine` class.

```python
class AbstractEngine:
    async def connect(self): ...
    async def disconnect(self): ...
    async def execute(self, query: str, params: tuple = ()): ...
    async def fetchone(self, query: str, params: tuple = ()): ...
    async def fetchall(self, query: str, params: tuple = ()): ...
```

---

### ✅ `async_engine.py`

Implements `AsyncMariaDBEngine`, extending `AbstractEngine`.

* Uses connection pool from `pool.py`
* Runs retry from `retry.py`
* Calls hooks from `hooks.py`
* Logs via `logger.py`
* Sends metrics via `metrics.py`

```python
from .abstract import AbstractEngine
from .pool import get_connection
from .retry import with_retry
from .hooks import before_hook, after_hook
from .logger import log_query
from .metrics import record_metric

class AsyncMariaDBEngine(AbstractEngine):
    async def execute(self, query, params=()):
        await before_hook(query, params)
        async with get_connection() as conn:
            result = await with_retry(conn.execute, query, params)
        await after_hook(query, params, result)
        log_query(query)
        record_metric("query_exec", query)
        return result
```

---

### ✅ `pool.py`

Manages async connection pooling.

```python
from asyncmy.pool import create_pool

_pool = None

async def init_pool(dsn, **kwargs):
    global _pool
    _pool = await create_pool(dsn=dsn, **kwargs)

async def get_connection():
    async with _pool.acquire() as conn:
        async with conn.cursor() as cur:
            yield cur

async def close_pool():
    _pool.close()
    await _pool.wait_closed()
```

---

### ✅ `retry.py`

Implements retry logic with backoff.

```python
import asyncio

async def with_retry(fn, *args, retries=3, delay=0.5, **kwargs):
    for attempt in range(retries):
        try:
            return await fn(*args, **kwargs)
        except Exception as e:
            if attempt == retries - 1:
                raise e
            await asyncio.sleep(delay * (2 ** attempt))
```

---

### ✅ `hooks.py`

Defines pre/post query execution hooks.

```python
async def before_hook(query, params):
    # Validate, enrich, log, etc.
    pass

async def after_hook(query, params, result):
    # Clean up, transform, emit event, etc.
    pass
```

---

### ✅ `logger.py`

Handles query logging (including slow queries).

```python
import time, logging

SLOW_QUERY_THRESHOLD = 1.0  # seconds
logger = logging.getLogger("db")

def log_query(query, start_time=None):
    duration = time.time() - start_time if start_time else None
    if duration and duration > SLOW_QUERY_THRESHOLD:
        logger.warning(f"SLOW QUERY ({duration:.2f}s): {query}")
    else:
        logger.info(f"QUERY: {query}")
```

---

### ✅ `metrics.py`

Integrates with metrics providers (e.g., Prometheus, OpenTelemetry).

```python
def record_metric(name, value):
    # Send to external monitoring system
    print(f"[METRIC] {name}: {value}")
```

---

### ✅ `health.py`

Provides health check hooks for uptime monitoring.

```python
from .pool import get_connection

async def check_db_health():
    try:
        async with get_connection() as conn:
            await conn.execute("SELECT 1")
        return True
    except:
        return False
```

---

## ✅ Optional: Usage in `main.py`

```python
from core.database.mariadb import async_engine, pool

async def startup():
    await pool.init_pool(dsn="your-mariadb-connection-string")
    db = async_engine.AsyncMariaDBEngine()
    await db.execute("SELECT * FROM users")

async def shutdown():
    await pool.close_pool()
```

---

Would you like a **fully working zip scaffold**, **FastAPI integration**, or **unit tests** next?
