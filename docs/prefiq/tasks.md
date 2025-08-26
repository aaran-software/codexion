awesome — let’s blueprint **Devmeta** (project manager) end‑to‑end so you can say “code next” when ready. This is a practical, implementation‑ready plan that matches your current Prefiq stack (providers, routers, migrations, multi‑DB support).

# Devmeta — Product Spec & Workflow

## Core concepts

* **Lead → Project**: when a lead converts, we create a **Project**.
* **Project** holds scope, dates, status, owner, linked client/lead.
* **Tasks** belong to a Project; each task has assignees, status, due dates.
* **Comments/Replies** on tasks for review/feedback loops.
* **Status tracking** for both Project and Task with lightweight state machines.
* **Activity log** for auditability.
* **People** (users) & **Teams** (optional) for assignment & visibility.
* **Attachments** (optional now; stub hooks).
* **Notifications** (events emitted; simple in‑app feed initially).
* **Multi‑tenant ready** (tenant\_id on rows; later can be enforced via middleware).

---

## Roles & permissions (MVP)

* **Admin**: full access within tenant.
* **Manager**: create/edit projects & tasks, assign people.
* **Member**: view & update own tasks, comment.
* **Viewer**: read‑only.

(We’ll enforce via simple role checks in request context; map later to your auth/JWT.)

---

## Status lifecycles

### Project status (finite state machine)

`draft → planned → in_progress → on_hold → completed → cancelled`

Allowed transitions:

* draft → planned | cancelled
* planned → in\_progress | on\_hold | cancelled
* in\_progress → on\_hold | completed | cancelled
* on\_hold → in\_progress | cancelled
* completed/cancelled → (terminal; only Admin can reopen to planned)

### Task status

`todo → in_progress → in_review → done → blocked`

* todo → in\_progress
* in\_progress → in\_review | blocked
* in\_review → done | in\_progress
* blocked → in\_progress
* done (terminal unless Manager/Admin reopens to in\_progress)

---

## Data model (tables & fields)

### projects

* id (pk)
* tenant\_id (fk)
* code (unique per tenant, e.g., `PRJ-2025-001`)
* title (str, 200)
* description (text)
* status (enum: as above)
* lead\_id (nullable, link to lead if exists)
* owner\_id (fk → users)
* priority (enum: low/normal/high/urgent)
* start\_date (date, nullable)
* due\_date (date, nullable)
* budget\_amount (decimal, nullable)
* custom\_fields (json, nullable)
* created\_at, updated\_at, deleted\_at (soft delete)

Indexes: (tenant\_id, code uniq), (tenant\_id, status), (tenant\_id, owner\_id)

### tasks

* id (pk)
* tenant\_id (fk)
* project\_id (fk → projects)
* title (str, 200)
* description (text)
* status (enum: task statuses)
* priority (enum)
* reporter\_id (fk → users)
* due\_date (date, nullable)
* estimate\_hours (int, nullable)
* order\_index (int, for kanban ordering)
* created\_at, updated\_at, deleted\_at

Indexes: (tenant\_id, project\_id, status), (tenant\_id, due\_date)

### task\_assignees

* id (pk)
* tenant\_id (fk)
* task\_id (fk)
* user\_id (fk)
* assigned\_at

Unique: (tenant\_id, task\_id, user\_id)

### comments

* id (pk)
* tenant\_id (fk)
* project\_id (fk)
* task\_id (fk, nullable for project‑level comments)
* author\_id (fk)
* body (text)
* attachments (json, nullable)
* created\_at, updated\_at

Index: (tenant\_id, task\_id), (tenant\_id, project\_id)

### activity\_logs

* id (pk)
* tenant\_id
* actor\_id (fk)
* object\_type (enum: project|task|comment)
* object\_id
* action (str: created|updated|status\_changed|assigned|commented|deleted|restored)
* meta (json: diff/status\_from/to/etc)
* created\_at

### users (reference)

Assume you already have users; otherwise define minimal: id, tenant\_id, name, email, role.

---

## API design (REST, JSON)

**Base prefixes** (mounted by DevmetaProvider):

* Web (HTML/JSON lightweight): `/devmeta`
* API (JSON): `/api/devmeta`

### Projects

* `POST /api/devmeta/projects`
  Create a project from a converted lead or manual.

  ```json
  {
    "title": "Website revamp",
    "description": "Refresh brand site",
    "lead_id": 123,
    "owner_id": 7,
    "priority": "high",
    "start_date": "2025-09-01",
    "due_date": "2025-11-30"
  }
  ```
* `GET /api/devmeta/projects` (filters: status, owner\_id, q, due\_before/after, page)
* `GET /api/devmeta/projects/{id}`
* `PATCH /api/devmeta/projects/{id}` (editable fields; status guarded by FSM)
* `DELETE /api/devmeta/projects/{id}` (soft delete)
* `POST /api/devmeta/projects/{id}/status`

  ```json
  {"to":"in_progress","reason":"Kickoff done"}
  ```
* `GET /api/devmeta/projects/{id}/tasks` (list)

### Tasks

* `POST /api/devmeta/projects/{id}/tasks`

  ```json
  {
    "title": "Design wireframes",
    "description": "Homepage + pricing",
    "priority": "high",
    "due_date": "2025-09-20",
    "assignees": [12, 19]
  }
  ```
* `GET /api/devmeta/tasks?project_id=...&status=...`
* `GET /api/devmeta/tasks/{task_id}`
* `PATCH /api/devmeta/tasks/{task_id}`
* `POST /api/devmeta/tasks/{task_id}/status`

  ```json
  {"to":"in_review","note":"ready for review"}
  ```
* `POST /api/devmeta/tasks/{task_id}/assignees` (add/remove)

  ```json
  {"add":[42], "remove":[19]}
  ```

### Comments / Reviews

* `POST /api/devmeta/tasks/{task_id}/comments`

  ```json
  {"body":"Looks good, fix spacing in hero."}
  ```
* `GET /api/devmeta/tasks/{task_id}/comments`
* `PATCH /api/devmeta/comments/{id}`
* `DELETE /api/devmeta/comments/{id}`

### Activity

* `GET /api/devmeta/projects/{id}/activity`
* `GET /api/devmeta/tasks/{id}/activity`

---

## Web routes (quick)

* `GET /devmeta` → project list (filters, search, counts by status).
* `GET /devmeta/projects/{id}` → project overview (status, timeline, tasks, activity).
* Optional: `/devmeta/board/{id}` → task kanban.

(Keep web handlers lightweight; frontends can be server‑rendered JSON or pull from API.)

---

## Provider & routing wiring

**DevmetaProvider.boot()** will:

* `include_routes("apps.devmeta.routes.web", prefix="/devmeta")`
* `include_routes("apps.devmeta.routes.api", prefix="/api/devmeta")`
* Bind services: `project_service`, `task_service`, `activity_service`, `notification_service` to Application container.
* Register FSM guards for status changes.

**Route modules** must use relative paths:

```python
# apps/devmeta/routes/api.py
from fastapi import APIRouter, Depends
router = APIRouter()

@router.get("/projects")
def list_projects(...): ...

@router.post("/projects")
def create_project(...): ...
```

---

## Services (use cases)

### ProjectService

* create\_project(data, actor) → project
* update\_project(id, patch, actor)
* change\_status(id, to, reason, actor)  \[validates FSM]
* delete\_project(id, actor)
* list\_projects(filters, page)
* get\_project(id)

### TaskService

* create\_task(project\_id, data, actor)
* update\_task(task\_id, patch, actor)
* change\_status(task\_id, to, note, actor)  \[FSM]
* set\_assignees(task\_id, add\[], remove\[], actor)
* list\_tasks(filters)
* get\_task(task\_id)

### CommentService

* add\_comment(task\_id, body, attachments, actor)
* edit\_comment(id, body, actor)
* delete\_comment(id, actor)

### ActivityService

* log(actor, object\_type, object\_id, action, meta)
* list\_for\_object(object\_type, object\_id)

### NotificationService (stub)

* emit(event\_name, payload)  (later: email/webhook)

All services take `tenant_id` (from auth context) to enforce isolation.

---

## Validation & guards

* **FSM**: deny illegal transitions; return `409 Conflict` + message.
* **Date checks**: due\_date ≥ start\_date.
* **Soft delete**: only Admin/Manager can delete; restore endpoint optional later.
* **Assignment**: only Manager/Admin can assign; Member can self‑assign if allowed flag set.

---

## List & search (server‑side filters)

Projects:

* `q` in `title/description`
* `status`, `owner_id`, `priority`
* `due_before`, `due_after`
* paging: `page`, `page_size` (default 20)

Tasks:

* `project_id`, `status`, `assignee_id`, `reporter_id`, `due_before/after`, `q`

Return envelope:

```json
{
  "data": [...],
  "page": 1,
  "page_size": 20,
  "total": 137
}
```

---

## Activity events (examples)

* `project.created`, `project.updated`, `project.status_changed`
* `task.created`, `task.updated`, `task.status_changed`, `task.assignees_changed`
* `comment.added`, `comment.edited`, `comment.deleted`

`meta` suggestions:

```json
{"from":"planned","to":"in_progress","reason":"Kickoff complete"}
```

---

## Migrations (per your builder)

Create these migration files under `apps/devmeta/database/migrations`:

1. `20250826_0001_projects.py`
2. `20250826_0002_tasks.py`
3. `20250826_0003_task_assignees.py`
4. `20250826_0004_comments.py`
5. `20250826_0005_activity_logs.py`

Each uses your engine‑agnostic builder API (SQLite/MariaDB/Postgres variants already done). We’ll generate the exact code when you say **code next**.

---

## Multi‑tenant considerations

* Every table includes `tenant_id`.
* Index `tenant_id` first in compound indexes for fast filtering.
* In API, resolve `tenant_id` from JWT/ctx; all queries must include it.
* (Optional) add a request dependency that injects `TenantContext` and guard queries.

---

## Non‑functional

* **Pagination & sorting** (by `created_at`, `due_date`, `priority`).
* **OpenAPI** auto docs — ensure tags set (`devmeta:web`, `devmeta:api`).
* **Idempotency**: allow `code` to be provided on project creation; enforce unique per tenant.
* **Soft delete** + (optional) restore endpoints later.
* **Optimistic concurrency** (optional): `updated_at` check on PATCH.

---

## Milestones & TODO (build order)

### M1 — Scaffolding & routes

* [x] Create `apps/devmeta/` scaffold (if not exists).
* [x] Implement `DevmetaProvider.boot()` with route includes.
* [x] Add `apps.cfg` section `[devmeta]` (already there).
* [x] Create `routes/web.py` (list page & health ping).
* [x] Create `routes/api.py` with empty handlers returning 501.

### M2 — Database schema

* [x] Write 5 migrations for projects, tasks, task\_assignees, comments, activity\_logs.
* [x] `prefiq run migrate --fresh` and verify with `doctor migrate`.

### M3 — Services & guards

* [ ] Implement `ProjectService`, `TaskService`, `CommentService`, `ActivityService`.
* [ ] Register services in provider `register()`.
* [ ] Add FSM validators for project/task status transitions.

### M4 — API endpoints

* [ ] Projects: create/list/get/patch/delete/status
* [ ] Tasks: create/list/get/patch/status/assignees
* [ ] Comments: add/list/edit/delete
* [ ] Activity: list per project/task

### M5 — Security & tenant

* [ ] Request dependency to extract `tenant_id` and `user` from JWT or stub.
* [ ] Role checks in service methods (Admin/Manager/Member/Viewer).

### M6 — UX quick views

* [ ] `/devmeta` project list with filters (server JSON to start).
* [ ] `/devmeta/projects/{id}` overview (server JSON).

### M7 — Polishing

* [ ] Pagination, sorting, search.
* [ ] Activity log integration on all mutations.
* [ ] Basic notification stubs (log events for now).

### M8 — Optional

* [ ] Kanban endpoints for task ordering.
* [ ] Attachments (file table or object storage links).
* [ ] Webhooks.

---

## Example flows

### Convert lead → start project

1. `POST /api/devmeta/projects` with `lead_id`.
2. Auto status `planned`, owner = creator by default.
3. Activity `project.created`.
4. Add initial tasks; assign.
5. `POST /api/devmeta/projects/{id}/status {"to":"in_progress"}` — kick off.

### Work cycle on a task

1. Assignee moves `todo → in_progress`.
2. Submits `in_progress → in_review` with comment.
3. Reviewer comments; either `in_review → done` or back to `in_progress`.
4. Activity tracks each step.

---

If this matches your expectations, say **“code next”** and I’ll generate:

* The 5 migration files (SQLite/MariaDB/Postgres compatible via your builder).
* `DevmetaProvider` with proper bindings.
* `routes/api.py` + `routes/web.py` with working endpoints (including validation/FSM).
* Service classes wired into the container.
* Minimal auth/tenant dependency stubs so you can run it immediately.
