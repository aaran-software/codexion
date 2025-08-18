# 📋 DevMeta

### 📦 Setup & Foundation

* [ ] Create folder structure under `apps/devmeta/` with `__init__.py` files.
* [ ] Add `provider.py` → define `DevMetaProvider` (register SQLite profile, migrator, todo service, CLI).
* [ ] Add `cli/devmeta.py` → Typer subapp (`migrate`, `todo add`, `todo list`, `todo done`).
* [ ] Update global CLI → mount `devmeta` subapp from `apps/devmeta/cli/devmeta:app`.
* [ ] Update settings → add `profiles.database.devmeta` (engine=sqlite, path=./.prefiq/devmeta.sqlite).

---

### 🗄️ Database & Migrations

* [ ] Add `migrations/0001_todos.sql` → create `todos` table (`id`, `title`, `status`, `priority`, `project`, `due_at`, `created_at`, `updated_at`, `completed_at`).
* [ ] Add `migrations/0002_indexes.sql` → indexes (`status`, `due_at`).
* [ ] Add `migrations/0003_notes.sql` → `notes` table (id, title, content, tags, linked\_todo\_id).
* [ ] Add `migrations/0004_logs.sql` → `logs` table (id, action, details, created\_at, user).
* [ ] Add `migrations/0005_projects.sql` → `projects` table (id, name, description, status).
* [ ] Add `migrations/0006_assignees.sql` → `assignees` table (id, name/email, role).
* [ ] Add `migrations/0007_progress.sql` → track progress (entity\_type, entity\_id, percent\_done, updated\_at).
* [ ] Add `migrations/0008_reviews.sql` → review table (id, entity\_type, entity\_id, comments, rating, created\_at).
* [ ] Add `migrations/0009_roadmap.sql` → roadmap milestones (id, project\_id, title, due\_at, status).

---

### ⚙️ Services

* [ ] Add `services/todo.py` → `TodoService` with `add`, `list`, `done`, `assign`.
* [ ] Add `services/note.py` → `NoteService` with `add`, `list`, `link_to_todo`.
* [ ] Add `services/log.py` → `LogService` (append actions, fetch history).
* [ ] Add `services/project.py` → `ProjectService` (create, update, assign, track progress).
* [ ] Add `services/roadmap.py` → `RoadmapService` (create milestone, update status).
* [ ] Add `services/review.py` → `ReviewService` (add review, list reviews).

---

### 🖥️ CLI Expansion

* [ ] `prefiq devmeta todo add/list/done/assign`
* [ ] `prefiq devmeta note add/list/link`
* [ ] `prefiq devmeta log list`
* [ ] `prefiq devmeta project create/list/progress`
* [ ] `prefiq devmeta roadmap add/list/status`
* [ ] `prefiq devmeta review add/list`

---

### 🌐 API Layer

* [ ] Create `api/` inside `apps/devmeta/` using FastAPI (mounted as optional).
* [ ] Endpoints for:

  * `/todos` (CRUD)
  * `/notes` (CRUD, linked to todos/projects)
  * `/logs` (read-only)
  * `/projects` (CRUD, progress)
  * `/roadmap` (CRUD milestones)
  * `/reviews` (add, list)
* [ ] Auth (simple token first → later integrate with prefiq users).

---

### 🎨 React UI (frontend client)

* [ ] Scaffold `devmeta-ui/` (React + Vite + Tailwind).
* [ ] Create shared API client for talking to FastAPI.
* [ ] Pages:

  * Dashboard (overview: todos, projects, roadmap).
  * Todos (list, add, mark done, assign).
  * Notes (list, editor).
  * Logs (timeline of activity).
  * Projects (details, progress bar).
  * Roadmap (milestones timeline).
  * Reviews (feedback board).
* [ ] Authentication (login, API token).

---

### 🧩 Integration & Collaboration

* [ ] Sync logs with Git commits (optional hook: save commit msg to logs).
* [ ] Export roadmap/progress as Markdown/CSV for team sharing.
* [ ] Enable CLI → API → UI sync (so all three surfaces work).
* [ ] Add team configuration (assignees sync).

---

### 🚀 Future Enhancements

* [ ] Notifications (email/Slack when todos assigned or deadlines near).
* [ ] Tagging system (labels for todos, notes, projects).
* [ ] Search across todos/notes/logs.
* [ ] Analytics dashboard (burn-down charts, progress graphs).
* [ ] Templates for project setup (ERP-style scaffolding).

---

awesome — here’s the **folder skeleton** for `apps/devmeta/` exactly as we planned (no code inside, just structure). I’m also giving you a one-shot **bash script** to create everything locally.

# 🗂️ Repo tree (skeleton only)

```
apps/
└─ devmeta/
   ├─ README.md
   ├─ __init__.py
   ├─ provider.py                    # DevMetaProvider (register/boot; binds migrator/services/cli)
   │
   ├─ cli/
   │  ├─ __init__.py
   │  └─ devmeta.py                  # Typer subapp: migrate, todo add/list/done
   │
   ├─ migrations/
   │  ├─ 0001_todos.sql              # create todos table
   │  └─ 0002_indexes.sql            # indexes for status, due_at
   │
   ├─ services/
   │  ├─ __init__.py
   │  └─ todo.py                     # TodoService (add, list, done) – MVP
   │
   ├─ api/                           # (stage-2+: FastAPI; optional now)
   │  ├─ __init__.py
   │  ├─ server.py                   # FastAPI app factory/mount (later)
   │  └─ routers/
   │     ├─ __init__.py
   │     ├─ todos.py
   │     ├─ notes.py
   │     ├─ logs.py
   │     ├─ projects.py
   │     ├─ roadmap.py
   │     └─ reviews.py
   │
   ├─ models/                        # (optional DTOs / enums later)
   │  ├─ __init__.py
   │  └─ dto.py
   │
   └─ sync/                          # (stage-2+: export/import NDJSON)
      ├─ __init__.py
      └─ ndjson.py
```

# ⚙️ Bash script to create the skeleton

> Run this from your **repo root** (where the `apps/` folder should live).

```
#!/bin/bash
mkdir -p apps/devmeta/{cli,migrations,services,api/routers,models,sync}

# top-level files
touch apps/devmeta/README.md
touch apps/devmeta/__init__.py
touch apps/devmeta/provider.py

# CLI
touch apps/devmeta/cli/__init__.py
touch apps/devmeta/cli/devmeta.py

# migrations (placeholders)
cat > apps/devmeta/migrations/0001_todos.sql <<'SQL'
-- TODO: create table todos (id, title, status, priority, project, due_at, created_at, updated_at, completed_at)
SQL
cat > apps/devmeta/migrations/0002_indexes.sql <<'SQL'
-- TODO: create indexes on todos(status) and todos(due_at)
SQL

# services
touch apps/devmeta/services/__init__.py
touch apps/devmeta/services/todo.py

# API (placeholders for future)
touch apps/devmeta/api/__init__.py
touch apps/devmeta/api/server.py
touch apps/devmeta/api/routers/__init__.py
touch apps/devmeta/api/routers/todos.py
touch apps/devmeta/api/routers/notes.py
touch apps/devmeta/api/routers/logs.py
touch apps/devmeta/api/routers/projects.py
touch apps/devmeta/api/routers/roadmap.py
touch apps/devmeta/api/routers/reviews.py

# models / sync (placeholders)
touch apps/devmeta/models/__init__.py
touch apps/devmeta/models/dto.py
touch apps/devmeta/sync/__init__.py
touch apps/devmeta/sync/ndjson.py

echo "✅ devmeta skeleton created under apps/devmeta/"
```

# 🔖 Notes

* This is **structure only** (as you asked). We’ll wire it to **prefiq** providers/CLI/logging when you say the word.
* Next step (when you say “code”): implement `provider.py`, MVP migrations `0001/0002`, `services/todo.py`, and `cli/devmeta.py` commands to get `prefiq devmeta migrate` + `todo add/list/done` working.
