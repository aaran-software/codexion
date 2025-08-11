# Database Layer Documentation

**Author**: ChatGPT
**Created**: 2025-08-06

## Overview

This document summarizes the architecture and implementation of the database engine system, designed for flexible, multi-driver support across synchronous and asynchronous Python applications.

---

## 1. Configuration Loader

### 📁 Module: `core/database/config_loader`

### ✅ Purpose:

* Centralized and dynamic configuration loader for all supported databases.
* Thread-safe, context-aware with override support.

### Components:

* **`base.py`**: Loads config from env or passed args; supports thread-local overrides.
* **Drivers (`drivers/*.py`)**: MariaDB, PostgreSQL, SQLite, MongoDB specific config extractors.

### Usage:

```python
from core.database.config_loader.base import use_thread_config
config = use_thread_config().get_config_dict()
```

---

## 2. Abstract Engine

### 📁 Module: `database/engines/abstract_engine.py`

### ✅ Purpose:

* Defines a unified interface for all engines.
* Provides lifecycle methods and hook support.

### Key Methods:

* `connect()`, `close()`
* `execute()`, `fetchone()`, `fetchall()`, `executemany()`
* `begin()`, `commit()`, `rollback()`
* `test_connection()`

---

## 3. Sync Engine (MariaDB)

### 📁 Module: `engines/mariadb/sync_engine.py`

### ✅ Purpose:

* Implements `AbstractEngine` for synchronous applications.
* Uses retry, logging, and hooks.

### Features:

* Retry with exponential backoff
* Slow query logging
* Config auto-injection from `config_loader`

---

## 4. Async Engine (MariaDB)

### 📁 Module: `engines/mariadb/async_engine.py`

### ✅ Purpose:

* Async-compatible MariaDB engine using context-managed pooled connections.

### Features:

* Uses `run_sync` to wrap blocking calls
* Integrated with `get_connection()` pool
* Supports retry, logging, hooks

---

## 5. Connection Pool

### 📁 Module: `engines/mariadb/pool.py`

### ✅ Purpose:

* Lightweight async-compatible pool wrapper.
* Based on thread-safe per-call connection via `anyio.to_thread.run_sync()`.

### Highlights:

* `init_pool(config)` stores config
* `get_connection()` returns context-managed cursor

---

## 6. Retry Logic

### 📁 Module: `retry.py`

### ✅ Purpose:

* Wrap DB operations with retry support

### Functions:

* `with_retry()` — sync
* `with_retry_async()` — async

### Features:

* Exponential backoff
* Graceful failure on max retries

---

## 7. Query Logger

### 📁 Module: `logger.py`

### ✅ Purpose:

* Log SQL query duration
* Warn for slow queries

### Example:

```python
log_query(query, start_time)
```

---

## 8. Hooks

### 📁 Module: `hooks.py`

### ✅ Purpose:

* Provides default before/after hooks for query execution.

### Usage:

```python
engine.set_before_execute_hook(default_before_hook)
engine.set_after_execute_hook(default_after_hook)
```

---

## 9. Health Check

### 📁 Module: `health.py`

### ✅ Purpose:

* Safely test engine health.

### Function:

```python
is_healthy(engine) -> bool
```

---