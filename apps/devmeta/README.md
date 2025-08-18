awesome — i went through your current state and marked what’s **done**, what’s **pending**, and added the missing pieces so the roadmap is complete and accurate for your *root-level `apps/devmeta`* app that reuses Prefiq.

---

# 📋 DevMeta — Master TODO (updated)

### 📦 Setup & Foundation

* [✅] Create folder structure under `apps/devmeta/` with `__init__.py` files.
* [✅] Add **core/provider.py** → `DevMetaProvider` (resolves SQLite path, binds migrator & services, mounts CLI).
* [✅] Add **cli/devmeta.py** → Typer subapp **and** mount helper (idempotent).
* [ ] Update global CLI → mount `devmeta` subapp from `apps/devmeta/cli/devmeta:app` (ensure main CLI container exposes `cli.app` or `cli` and that `DevMetaProvider.boot()` is called).
* [ ] Update settings → add `profiles.database.devmeta` (engine=sqlite, **path=apps/devmeta/data/devmeta.sqlite**) and/or set `PREFIQ_DEV_SQLITE` env var.

### 🗄️ Database & Migrations

* [✅] **database/migration/m000\_migrations\_tbl.py** → create & ensure `dev_migrations` table (bootstrap).
* [ ] **migrations/0001\_todos.sql** → create `todos` table:
  `id, title, status, priority, project, due_at, created_at, updated_at, completed_at`.
* [ ] **migrations/0002\_indexes.sql** → indexes on `status`, `due_at`.
* [ ] **migrations/0003\_notes.sql** → `notes` table (id, title, content, tags/json, linked\_todo\_id).
* [ ] **migrations/0004\_logs.sql** → `logs` table (id, level, message/details, context/json, created\_at, user).
* [ ] **migrations/0005\_projects.sql** → `projects` table (id, key, name, description, status).
* [ ] **migrations/0006\_assignees.sql** → `teammates/assignees` table (id, handle, name, email, role).
* [ ] **migrations/0007\_progress.sql** → `progress` (entity\_type, entity\_id, percent\_done, updated\_at).
* [ ] **migrations/0008\_reviews.sql** → `reviews` (id, entity\_type, entity\_id, comments, rating, created\_at).
* [ ] **migrations/0009\_roadmap.sql** → `roadmap_milestones` (id, project\_id, title, due\_at, status).

### ⚙️ Services

* [ ] **services/todo.py** → `TodoService` with `add`, `list`, `done`, *(optional: `assign` later when teammates exist)*.
* [ ] **services/note.py** → `NoteService` with `add`, `list`, `link_to_todo`.
* [ ] **services/log.py** → `LogService` (append actions, fetch history).
* [ ] **services/project.py** → `ProjectService` (create, update, attach progress).
* [ ] **services/roadmap.py** → `RoadmapService` (add milestone, update status).
* [ ] **services/review\.py** → `ReviewService` (add review, list reviews).

### 🖥️ CLI Expansion

* [ ] `prefiq devmeta migrate`
* [ ] `prefiq devmeta todo add`
* [ ] `prefiq devmeta todo list`
* [ ] `prefiq devmeta todo done`
* [ ] *(later)* `prefiq devmeta todo assign`
* [ ] *(later)* `prefiq devmeta note add/list/link`
* [ ] *(later)* `prefiq devmeta log list`
* [ ] *(later)* `prefiq devmeta project create/list/progress`
* [ ] *(later)* `prefiq devmeta roadmap add/list/status`
* [ ] *(later)* `prefiq devmeta review add/list`

### 🌐 API Layer (later)

* [ ] Create `api/server.py` (FastAPI app factory; optional mount into main API).
* [ ] Endpoints:

  * `/todos` (CRUD)
  * `/notes` (CRUD, link to todo/project)
  * `/logs` (read-only)
  * `/projects` (CRUD, progress)
  * `/roadmap` (CRUD milestones)
  * `/reviews` (add, list)
* [ ] Auth: simple token (env) → later integrate with Prefiq users/session.

### 🎨 React UI (later)

* [ ] Scaffold `devmeta-ui/` (Vite + React + Tailwind).
* [ ] Shared API client.
* [ ] Pages: Dashboard, Todos, Notes, Logs, Projects, Roadmap, Reviews.
* [ ] Auth (token entry or login).

### 🧩 Integration & Collaboration

* \[✅] **sync/ndjson.py** → NDJSON export/import helpers.
* [ ] Add CLI for `prefiq devmeta export` / `prefiq devmeta import`.
* [ ] Optional: Git hook to push commit messages into `logs`.
* [ ] Export roadmap/progress as Markdown/CSV.
* [ ] Ensure consistency across CLI ↔ API ↔ UI.

### 🧱 Core Utilities / Models

* \[✅] **core/helper.py** → `resolve_sqlite_path`, `ensure_dir_for`, `connect_sqlite`, `sha256_file`.
* \[✅] **models/todo.py** → dataclass model & helpers.
* \[✅] **cli/devmeta.py** → Typer subapp + `mount_devmeta_cli(container)` idempotent mounting.
* \[✅] **core/provider.py** (refactored) → resolves path, binds migrator & todo service (when present), mounts CLI.
* [ ] Ensure **apps/devmeta/data/** folder exists in repo (commit `.gitkeep`; DB file will be created by migrate).

### ✅ What’s already implemented (recap)

* Provider (core/provider.py) — **done**
* Helpers (core/helper.py) — **done**
* Migration bootstrap table (database/migration/m000\_migrations\_tbl.py) — **done**
* CLI subapp & mount helper (cli/devmeta.py) — **done**
* NDJSON export/import (sync/ndjson.py) — **done**
* Todo dataclass model (models/todo.py) — **done**
* Path decision: SQLite at `apps/devmeta/data/devmeta.sqlite` — **done**

---

## 🔜 Immediate next steps (to get MVP running)

1. **Write the actual SQL migrations**

   * [ ] `apps/devmeta/migrations/0001_todos.sql`
   * [ ] `apps/devmeta/migrations/0002_indexes.sql`

2. **Implement TodoService**

   * [ ] `apps/devmeta/services/todo.py` with `add`, `list`, `done`
   * Ensure `DevMetaProvider.register()` imports and binds it.

3. **Wire CLI commands**

   * [ ] In `apps/devmeta/cli/devmeta.py`, add:

     * `@app.command("migrate")` → resolves `devmeta.migrator` and runs `migrate()`
     * `@app.command("todo-add")`, `@app.command("todo-list")`, `@app.command("todo-done")`

4. **Mount provider & CLI**

   * [ ] Confirm your main bootstrap registers `DevMetaProvider`
   * [ ] Ensure container exposes `cli.app` or `cli` so `mount_devmeta_cli()` can attach

5. **Smoke test**

   * [ ] `prefiq devmeta migrate`
   * [ ] `prefiq devmeta todo-add "First task"`
   * [ ] `prefiq devmeta todo-list`
   * [ ] `prefiq devmeta todo-done 1`

---

If you want, I can now **write the two migrations (0001/0002)** and **code `TodoService` + CLI commands** so your MVP runs end-to-end. Just say:
**“code migrations + todo service + cli commands”** and I’ll drop them in.
