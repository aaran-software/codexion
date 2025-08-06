# Schema Builder & Migration Layer

**Author**: ChatGPT
**Created**: 2025-08-06

## Overview

This system introduces a fluent-style schema builder for defining and managing database schema migrations in a raw SQL environment. It abstracts SQL generation for common field types and migration operations, inspired by Laravel migrations.

---

## Components

### ✅ 1. `blueprint.py`

* Defines `TableBlueprint`, the core class for building schema via method chaining.
* Supports columns, foreign keys, unique constraints, indexes, timestamps, soft deletes, and enums.

#### Example:

```python
table.id()
table.string("name", length=255, nullable=False)
table.boolean("is_active", default=True)
table.timestamps()
```

---

### ✅ 2. `builder.py`

* Provides functions to define schema operations (`create`, `dropIfExists`) programmatically.

#### Example:

```python
create("users", lambda table: [
    table.id(),
    table.string("name"),
    table.timestamps()
])
```

* Uses `TableBlueprint` to build column definitions.
* Produces raw SQL like:

```sql
CREATE TABLE IF NOT EXISTS `users` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255),
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  ...
);
```

---

### ✅ 3. Migration Script (e.g., `user_table.py`)

* Each migration file exposes:

```python
def up():
    # define table creation

def down():
    # rollback by dropping
```

* Example:

```python
def up():
    create("users", lambda table: [
        table.id(),
        table.string("name"),
        table.timestamps()
    ])

def down():
    dropIfExists("users")
```

---

### ✅ 4. Migration Test (e.g., `test_create_users_table.py`)

* Validates migration correctness by asserting table existence.
* Example:

```python
def test_create_users_table():
    dropIfExists("users")
    create("users", lambda table: [...])
    assert db.fetchone("SHOW TABLES LIKE 'users'") is not None
```

---

## Planned Features

* ✅ Auto record applied migrations in a `migrations` table.
* ✅ Ordered execution of up/down methods.
* 🔄 CLI integration for `migrate`, `rollback`, `refresh`, `status`.
* 🔄 Dependency validation (foreign keys across files).
* 🔄 Dry-run mode.

---

## Benefits

* Clean, maintainable schema definition syntax.
* Works with any raw SQL backend.
* Migration rollback support.
* Separation of migration intent (up/down).

---

Let me know when ready to build CLI migration runner or schema diffing tool.
