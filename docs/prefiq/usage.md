# prefiq CLI — Usage Guide

This is a practical, copy‑pasteable guide for working with `prefiq` apps and their databases (SQLite, Postgres, MariaDB), migrations, and diagnostics.

---

## Install & Basics

```bash
# in your project venv
pip install -e .
# or if prefiq is a package on your index:
pip install prefiq
```

CLI shape:

```
prefiq <app> <command> [options]
```

Examples:

* `prefiq devmeta migrate --fresh`
* `prefiq myapp rollback --steps 1`
* `prefiq doctor`

Profiles (DEV/TEST/PROD) come from your app settings (commonly via env). Typical env knobs:

```bash
export PREFIQ_PROFILE=DEV
export PREFIQ_DB_URL=sqlite:///./dev.db
# or Postgres: postgres://user:pass@localhost:5432/mydb
# or MariaDB:  mysql+pymysql://user:pass@localhost:3306/mydb
```

---

## Quick Reference (Cheat Sheet)

```bash
# Health check
prefiq doctor

# Run all pending migrations
prefiq <app> migrate

# Fresh start (drop, recreate migrations table & all app tables, re-apply)
prefiq <app> migrate --fresh

# Apply N migration steps only (if supported)
prefiq <app> migrate --steps 2

# Roll back one step (or N steps)
prefiq <app> rollback
prefiq <app> rollback --steps 2

# Seed the database (if your migrator implements seeding)
prefiq <app> seed
prefiq <app> migrate --seed

# Show registered apps (if available)
prefiq apps list

# Drop app tables (if supported)
prefiq <app> drop

# Introspect connection & driver
prefiq db info
```

> Tip: Most commands accept `--help` for live usage.

---

## Core Commands

### `prefiq doctor`

Runs environment & connectivity checks:

* Verifies Python, packages, and logging.
* Validates DB connection using `PREFIQ_DB_URL`.
* Confirms app discovery/modules are importable.

**Use when:** set up a new machine, changed drivers, or migrations fail unexpectedly.

---

### `prefiq <app> migrate`

Applies all outstanding migrations for the given app.

**Useful flags**

* `--fresh`

  1. Drops the `migrations` registry (and app tables),
  2. Recreates schema,
  3. Reapplies all migrations in order.
* `--steps N`
  Applies only the next N migration steps (if your CLI/migrator exposes this).
* `--seed`
  After migrate, run seeding (if `Migrator.seed()` exists).

**Examples**

```bash
prefiq devmeta migrate
prefiq devmeta migrate --fresh
prefiq devmeta migrate --steps 1
prefiq devmeta migrate --fresh --seed
```

---

### `prefiq <app> rollback`

Rolls back the most recent migration(s).

**Flags**

* `--steps N` (default 1)

**Examples**

```bash
prefiq devmeta rollback        # rollback last step
prefiq devmeta rollback --steps 3
```

---

### `prefiq <app> seed`

Runs the seeding routine (if implemented). Often equivalent to `prefiq <app> migrate --seed`.

---

## Migration Authoring

**Location & Naming**

* Each app keeps its migrations in `apps/<app>/database/migrations/`.
* Typical file name pattern: `YYYYMMDD_HHMM_<slug>.py`
* Each file defines a `Migrations` subclass:

```python
from prefiq.database.migrations.base import Migrations

class Tasks(Migrations):
    APP_NAME    = "devmeta"
    TABLE_NAME  = "tasks"
    ORDER_INDEX = 2

    def up(self) -> None:
        self.create(self.TABLE_NAME, lambda t: [
            t.id(),
            t.biginteger("project_id"),
            t.string("title"),
            t.text("description", nullable=True),
            t.string("assignee", nullable=True),
            t.string("status", default="todo"),
            t.datetime("due_date", nullable=True),
            t.integer("priority", default=3),
            t.timestamps(),
            t.index("project_id"),                   # single-column index
            t.index(["project_id", "status"]),      # composite index
            # unique example:
            # t.unique("uniq_task_title_per_project", ["project_id", "title"]),
        ])

    def down(self) -> None:
        self.drop_if_exists(self.TABLE_NAME)
```

**Index API (consistent across SQLite / Postgres / MariaDB)**

* `t.index("col")` → creates `idx_<table>_<col>`
* `t.index(["col1", "col2"])` → creates `idx_<table>_<col1>_<col2>`
* `t.index("idx_custom_name", ["col1","col2"])` → explicit name

**Other helpers**

* Columns: `string`, `text`, `integer`, `biginteger`, `boolean`, `date`, `datetime`, `json` (JSONB on PG), `uuid`, etc.
* Constraints: `check(condition, name=None)`, `unique(name, [cols])`
* FKs (fluent):
  `t.foreign_id("project_id").references("projects", "id").on_delete("CASCADE")`
* Timestamps: `t.timestamps()` (creates `created_at`, `updated_at`)

  > Note: Postgres doesn’t auto-update `updated_at` — update it in app code or via triggers.

---

## Multi‑DB Notes

**SQLite**

* Quoting: `"` (double quotes)
* Indexes are created post‑table via `CREATE INDEX IF NOT EXISTS`.
* File or memory DBs via URL, e.g. `sqlite:///./dev.db` or `sqlite:///:memory:`.

**Postgres**

* Quoting: `"` (double quotes)
* Indexes created after table with `CREATE INDEX IF NOT EXISTS`.
* URL: `postgresql://user:pass@host:5432/dbname` (or `postgres://...`)

**MariaDB / MySQL**

* Quoting: `` `backticks` ``
* We inline indexes inside `CREATE TABLE` (and also expose `createIndex` helper if needed).
* URL: `mysql+pymysql://user:pass@host:3306/dbname`

---

## Typical Workflows

### Start clean (DEV)

```bash
export PREFIQ_PROFILE=DEV
export PREFIQ_DB_URL=sqlite:///./dev.db
prefiq doctor
prefiq devmeta migrate --fresh
```

### Apply the newest migration in a shared DB

```bash
export PREFIQ_DB_URL=postgres://user:pass@db:5432/prefiq
prefiq devmeta migrate
```

### Undo the last migration

```bash
prefiq devmeta rollback
```

### Seed after a fresh reset

```bash
prefiq devmeta migrate --fresh --seed
```

---

## Troubleshooting

* **`TypeError: TableBlueprint.index() missing 1 required positional argument: 'column'`**
  You’re likely calling `t.index("col")` but your blueprint expected `(name, column)`. Ensure your blueprint supports the flexible signature documented above.

* **Indexes not appearing (SQLite)**
  Confirm your SQLite builder calls `CREATE INDEX IF NOT EXISTS` using `table.index_meta` after `CREATE TABLE`.

* **`OptionInfo` vs int errors in CLI**
  Ensure your `prefiq ... migrate` wrapper passes resolved values (not Typer `OptionInfo`) into your internal migrator functions. The guide assumes that’s already in place.

* **Postgres `updated_at` not auto‑updating**
  Use the app layer to set `updated_at = NOW()` on writes, or install a trigger.

---

## Adding New Commands (pattern)

If you want to add a custom command to an app, follow the pattern used by existing CLIs (Typer / Click style). Example:

```python
# apps/devmeta/cli/devmeta.py
import typer
from prefiq.apps.devmeta.cli.devmetadatabase import dev_migrate, dev_rollback

app = typer.Typer(help="Devmeta CLI")

@app.command()
def migrate(fresh: bool = False, steps: int | None = None, seed: bool = False):
    dev_migrate(fresh=fresh, steps=steps, seed=seed)

@app.command()
def rollback(steps: int = 1):
    dev_rollback(steps=steps)

if __name__ == "__main__":
    app()
```

Then wire it into your `prefiq` top‑level entry so it routes `prefiq devmeta ...` to this Typer app.

---

## Safety & Idempotency Tips

* Prefer `CREATE TABLE IF NOT EXISTS` and `CREATE INDEX IF NOT EXISTS` where supported.
* Keep migration files **immutable** after they are applied in shared environments — add new files instead of editing old ones.
* Use deterministic index names to avoid collisions across reruns.

---

If you want this as a markdown file in your repo (e.g., `docs/prefiq-cli.md`) or as an in‑app `--help` explainer, say the word and I’ll format it to your preferred style (MkDocs, Docusaurus, README section, etc.).
