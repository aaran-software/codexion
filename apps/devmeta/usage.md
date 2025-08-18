Here’s how your **new CLI setup** is actually used end-to-end, now that we’ve mounted `devmeta` into the global `prefiq` CLI.

---

# 🚀 Usage Guide

### Base CLI

```bash
prefiq --help
```

Shows the root groups:

* `server` → your existing server commands
* `run` → operational commands (migrate, sanity, clear-cache)
* `devmeta` → **new** DevMeta group we just added

---

### Database Migrations

```bash
# Apply all pending DevMeta migrations
prefiq devmeta migrate

# Roll back the last migration
prefiq devmeta rollback

# Roll back N steps
prefiq devmeta rollback --steps 2
```

---

### Todos

```bash
# Add a todo
prefiq devmeta todo-add "Write docs" --priority 2 --project "alpha" --due-at 2025-08-25T10:00:00 --tags "docs,writing"

# List todos (all)
prefiq devmeta todo-list

# List only open todos
prefiq devmeta todo-list --status open

# Mark a todo as done
prefiq devmeta todo-done 1
```

---

### Other Root Commands (unchanged)

```bash
# Server
prefiq server run

# Run group
prefiq run migrate     # core database migrations
prefiq run sanity
prefiq run clear-cache
```

---

# 🧪 Quick Smoke Test Flow

```bash
# Apply migrations
prefiq devmeta migrate

# Add your first todo
prefiq devmeta todo-add "First task"

# List todos
prefiq devmeta todo-list

# Mark it done
prefiq devmeta todo-done 1
```

---

👉 Do you want me to also stub out the **`TodoService`** implementation so these `todo-*` commands actually hit your SQLite DB immediately? Right now the CLI is wired, but it needs that service bound in your `DevMetaProvider`.
