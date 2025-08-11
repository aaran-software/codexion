Perfect. Let’s **finalize the architecture** and layout **all files with purpose, responsibilities, and clear TODOs** — so you can proceed with implementation or delegate it efficiently.

This design is:

* ✅ **Scalable** for any number of apps/modules
* ✅ **Safe** with hash-tracking and rollback
* ✅ **Testable** with TDD
* ✅ **Extendable** for CLI, locks, tagging, etc.

---

## ✅ FINAL REPO STRUCTURE + FUNCTIONALITY

We'll split the core into **6 logical areas**:

---

### 1️⃣ `apps/<module>/database/migration/`

| File                 | Purpose                                         |
| -------------------- | ----------------------------------------------- |
| `001_user_table.py`  | DSL-based migration script                      |
| `migration_order.py` | Ordered list of migration names (without `.py`) |

**Example:**

```python
# apps/auth/database/migration_order.py
migration_order = [
    "001_user_table",
    "002_roles_table"
]
```

**Migration file:**

```python
# apps/auth/database/migration/001_user_table.py
from cortex.database.schemas.builder import create, dropIfExists

def up():
    create("users", lambda t: [
        t.id(),
        t.string("email"),
        t.boolean("is_active"),
        t.timestamps()
    ])

def down():
    dropIfExists("users")
```

---

### 2️⃣ `cortex/database/migrations/`

| File                       | Purpose                                                | TODO                                                                                                            |
| -------------------------- | ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| `runner.py`                | Runs `up()` migrations based on `migration_order.py`   | ✅ Create table if missing<br>✅ Track name/module/order/time/hash<br>✅ Validate all files exist<br>✅ Use builder |
| `rollback.py`              | Rolls back N most recent migrations via `down()`       | ✅ Load migration records<br>✅ Reverse order<br>✅ Call `down()`<br>✅ Remove from tracking                        |
| `utils.py`                 | Helper functions for hashing, loading, file resolution | ✅ File hashing (SHA256)<br>✅ Dynamic module loading<br>✅ Order validation                                       |
| `lock.py` *(optional)*     | Prevent concurrent migration execution                 | 🟡 File or DB-based lock mechanism                                                                              |
| `registry.py` *(optional)* | Central place to register all modules for CLI support  | 🟡 Loadable list of all apps/modules                                                                            |

---

### 3️⃣ `cortex/database/schemas/`

| File         | Purpose                                        | TODO                                                                               |
| ------------ | ---------------------------------------------- | ---------------------------------------------------------------------------------- |
| `builder.py` | DSL to create/drop tables (used by migrations) | ✅ Implement `create()` and `dropIfExists()`<br>✅ Internally uses `db.execute(...)` |
| `types.py`   | TableBuilder, ColumnBuilder etc.               | ✅ Map DSL to SQL strings<br>✅ Validate column types                                |

---

### 4️⃣ `cortex/database/connection.py`

* Resolves the `db` (sync/async)
* Used by `builder` internally

---

### 5️⃣ `cortex/core/settings.py`

* Provides DB\_ENGINE, DB\_HOST, etc.

---

### 6️⃣ `tests/`

| File                         | Purpose                                          |
| ---------------------------- | ------------------------------------------------ |
| `test_create_users_table.py` | TDD test for `migrate_table()`, `drop_migrate()` |
| `test_rollback.py`           | Tests `rollback(steps=N)`                        |

---

## ✅ MIGRATIONS TABLE SCHEMA

| Column        | Type        | Purpose                         |
| ------------- | ----------- | ------------------------------- |
| `id`          | INT PK      | Auto-increment                  |
| `module`      | VARCHAR     | e.g., `"auth"`                  |
| `name`        | VARCHAR     | e.g., `"001_user_table"`        |
| `order_index` | INT         | Order from `migration_order.py` |
| `applied_at`  | TIMESTAMP   | Auto-filled                     |
| `hash`        | VARCHAR(64) | SHA256 of file content          |

Created via `builder.create(...)` if missing.

---

## 🧠 FINAL TODOs (All Parts)

### 🧱 Migrations System (Core Logic)

* [ ] **`runner.py`**

  * [ ] Load `migration_order.py`
  * [ ] Validate files exist
  * [ ] Hash migration file
  * [ ] Check `migrations` table exists
  * [ ] Run `up()` if not applied
  * [ ] Insert record into `migrations` table

* [ ] **`rollback.py`**

  * [ ] Load last N from `migrations`
  * [ ] Run `down()` in reverse order
  * [ ] Remove from `migrations` table

* [ ] **`utils.py`**

  * [ ] `compute_hash(file_path) -> str`
  * [ ] `load_migration_module(path)`
  * [ ] `resolve_module_migration_path(module, name)`
  * [ ] `read_order_file(module)`

---

### 🧰 DSL Builder

* [ ] **`builder.py`**

  * [ ] `create(table_name: str, builder_fn)`
  * [ ] `dropIfExists(table_name: str)`
  * [ ] `db.execute(...)` under the hood

* [ ] **`types.py`**

  * [ ] Class `TableBuilder`

    * [ ] `.id()`
    * [ ] `.string(name)`
    * [ ] `.boolean(name)`
    * [ ] `.timestamps()`

---

### 🧪 Tests

* [ ] `test_create_users_table.py`

  * [x] `migrate_table("user", "auth")` works
  * [ ] Verifies table exists

* [ ] `test_rollback.py`

  * [ ] Rollback 1 or more steps
  * [ ] Table is removed
  * [ ] Record removed from `migrations` table

---

## 📦 Future-Proofing (Optional)

| Feature             | File / Concept       | Status                           |
| ------------------- | -------------------- | -------------------------------- |
| CLI entrypoint      | `scripts/migrate.py` | 🟡 Optional                      |
| Author metadata     | in migration file    | 🟡 Optional                      |
| Tagging/staging     | via `tags = []`      | 🟡 Optional                      |
| SQLite/Postgres/etc | Plug-in engine       | ✅ Supported via `db` abstraction |

---

## ✅ Summary

You are fully ready to build. Here's the suggested order of implementation:

### 🔢 Build Order

1. [ ] `utils.py`
2. [ ] `builder.py` + `types.py`
3. [ ] `runner.py` (with TDD test)
4. [ ] `rollback.py`
5. [ ] Migrations table bootstrapping
6. [ ] Test cases

---

Would you like me to begin implementing `utils.py` (hash + module loader), or the `builder.py` schema DSL next?
