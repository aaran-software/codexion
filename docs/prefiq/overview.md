# 🧠 Prefiq – Enterprise Framework

> **Goal:** Build a future‑proof, open-source friendly, enterprise‑grade platform.

- **Prefiq**: framework.
- **Cortex**: Main backend app (global admin).
- **Apps**: Self‑contained (bin + core + src), run individually on Prefiq or together under Cortex.
- **Resources/**: Shared assets for all apps.

---

## 🧭 Vision & Principles

Build a modular, future-proof enterprise platform where apps are self-contained products, unified by open standards and developer-friendly automation.

---

## 🏢 GitHub Organization Layout (Repos)

Use a GitHub org (e.g., `codexion`) with the following top-level repos:

| Repo              | Purpose                                                               | Public? | Notes                                              |
|-------------------|-----------------------------------------------------------------------|---------|----------------------------------------------------|
| **prefiq**        | 🔧 Pure Python framework kernel & CLI                                 | ✅       | Apache-2.0; pip package `prefiq`                   |
| **cortex**        | 🧠 Main backend app (global admin, users, settings, orchestration)    | ✅       | Depends on `prefiq`                                |
| **resources**     | 🗂️ Global shared assets (frontend + backend + themes)                | ✅       | NPM `@codexion/resources`, Py `codexion-resources` |
| **app-crm**       | 🤝 CRM app (bin/core/src)                                             | ✅       | Runs standalone or under Cortex                    |
| **app-erp**       | 🏭 ERP app (bin/core/src)                                             | ✅       | Ditto                                              |
| **app-ecommerce** | 🛒 Ecommerce app (bin/core/src)                                       | ✅       | Ditto                                              |
| **app-lms**       | 📚 LMS app (bin/core/src)                                             | ✅       | Ditto                                              |
| **app-ai**        | 🤖 AI services (bin/core/src)                                         | ✅       | Optional; model adapters & agents                  |
| **devops**        | 🚀 Deploy (Docker, Compose, Helm, Terraform), environments            | ✅       | Images: `ghcr.io/codexion/*`                       |
| **docs**          | 📘 Documentation site (Docusaurus/Mintlify)                           | ✅       | Autopublish to `docs.codexion.dev`                 |
| **starters**      | 🧪 Templates & scaffolds (project/app/site)                           | ✅       | `create-prefiq-app` scaffolder                     |
| **examples**      | 🔬 Example apps/integrations/playgrounds                              | ✅       | Learning & demos                                   |
| **meta**          | 🧩 Org standards (RFCs, ADRs, guidelines, issue templates)            | ✅       | Source of truth for conventions                    |

> 👇 You can start with **prefiq**, **cortex**, **resources**, and **app-crm**; add others as they mature.

---

## 🧬 Relationships (High-Level)

```
+-----------+        uses         +---------+     orchestrates     +--------------------+
|  prefiq   | <------------------ | cortex  | <------------------- |  apps (crm, erp...)|
| framework |                    /| control |\                    /|  bin/core/src       |
+-----------+                   / +---------+ \                  / +--------------------+
           ^                   /                \                /
           |                 serves             consumes      shares
           |                     \                /             |
           |                      \              /              v
           |                       +------------+        +-------------+
           |                       | resources  | <----> |  sites/*    |
           |                       +------------+        +-------------+
```

---

## 🧩 Core Conventions

### 📁 Per-App Structure (bin/core/src)

```
app-<name>/
├─ bin/                # Python backend runtime
│  ├─ api/             # REST/RPC endpoints
│  ├─ models/          # ORM models
│  ├─ services/        # domain services, jobs
│  ├─ migrations/      # DB migrations
│  ├─ config/          # app config, feature flags
│  └─ tests/
├─ core/               # Shared domain spec & logic
│  ├─ schema/          # JSON Schema + OpenAPI fragments
│  ├─ constants/
│  ├─ validation/      # language-agnostic rules (JSONLogic/ValRef)
│  ├─ types/           # generated types (py/ts) from schema
│  └─ docs/
└─ src/                # React/TS frontend
   ├─ app/             # routes, pages
   ├─ components/
   ├─ hooks/
   ├─ services/        # API clients generated from OpenAPI
   ├─ styles/
   └─ tests/
```

**Why this works:**

* **`core/`** becomes the single source of truth (schemas/validation) → generate **TS types**, **Pydantic models**, and
  **OpenAPI** → zero drift between FE & BE.
* **`bin/`** imports **`core/types/python`**; **`src/`** imports **`core/types/ts`**.

### 🧱 Shared Resources

```
resources/
├─ frontend/
│  ├─ components/   # design system (buttons, tables, forms)
│  ├─ hooks/
│  ├─ utils/
│  └─ styles/       # tokens, tailwind preset, themes
├─ backend/
│  ├─ emails/       # mjml/html templates
│  ├─ templates/    # pdf/report templates (Jinja)
│  └─ snippets/
├─ public/          # icons, logos, images, fonts
└─ themes/          # theme packs (json/yaml)
```

---

## 🧪 Tech Standards

* **Python**: 3.12+, `poetry`, `ruff`, `black`, `mypy`, `pytest`, `alembic`
* **Web**: Node 20+, `pnpm`, `vite`, `typescript`, `eslint`, `playwright`/`vitest`
* **API**: FastAPI (or Prefiq Router), OpenAPI 3.1, OAuth2/JWT, RBAC/ABAC
* **DB**: PostgreSQL, multi-tenant (db/schema/row-level; pluggable)
* **CI**: GitHub Actions; reusable workflows in `meta/.github/workflows`
* **Containers**: Dockerfiles per repo; Helm charts in `devops/helm`
* **Commits**: Conventional Commits (`feat:`, `fix:`), `commitlint`
* **Versioning**: SemVer; `release-please` for automated changelogs

---

## 📦 Repo-by-Repo Blueprints

### 1) **prefiq** (Framework) 🔧

```
prefiq/
├─ prefiq/
│  ├─ core/            # kernel, DI container, lifecycle
│  ├─ http/            # router, middleware, requests, responses
│  ├─ auth/            # auth primitives
│  ├─ orm/             # adapters (SQLAlchemy), repo pattern
│  ├─ events/          # event bus, subscribers
│  ├─ cli/             # `prefiq` command (Typer)
│  ├─ plugins/         # discovery (entry_points: prefiq.apps)
│  └─ utils/
├─ examples/
├─ docs/
├─ tests/
├─ pyproject.toml
└─ README.md
```

**Must-haves:**

* 🔌 **Plugin discovery** via `entry_points={'prefiq.apps': ['crm=app_crm.bin:Plugin']}`
* 🧵 **Request pipeline** (middleware), **Service providers**, **Config system**
* 🧪 First-class test harness & fake app loader
* 🧰 Codegen: `prefiq codegen` → OpenAPI clients & type stubs

**README.md (emoji sections):**

* ✨ Features
* 🚀 Quickstart
* 🧩 Architecture
* 🔌 Plugins
* 🧪 Testing
* 📦 Packaging & Versioning
* 🤝 Contributing
* 📜 License

---

### 2) **cortex** (Main Backend App) 🧠

```
cortex/
├─ cortex/
│  ├─ dashboard/
│  ├─ settings/
│  ├─ users/ (authz, RBAC/ABAC, orgs/teams)
│  ├─ notifications/
│  ├─ api/
│  ├─ migrations/
│  └─ config/
├─ tests/
├─ pyproject.toml
└─ README.md
```

**Responsibilities:** global admin UI backend, site registry, app registry, license/tenancy, audit/logging, job queue
admin.

**Protect Cortex:** Not inside `apps/` to avoid casual edits. Release as `cortex` package + Docker image.

---

### 3) **resources** (Shared) 🗂️

* Publishes **NPM** (`@codexion/resources`) and **PyPI** (`codexion-resources`).
* Frontend: design system (headless + Tailwind preset), icons, hooks.
* Backend: email/report templates, Jinja macros, PDF styles.

```
resources/
├─ packages/
│  ├─ frontend/      # NPM package
│  └─ backend/       # Python package
├─ public/
└─ README.md
```

---

### 4) **app-**\* (Product Apps) 🎛️

**Example: `app-crm`**

```
app-crm/
├─ bin/
│  ├─ api/
│  ├─ models/
│  ├─ services/
│  ├─ migrations/
│  ├─ config/
│  └─ tests/
├─ core/
│  ├─ schema/          # JSON Schema + OpenAPI fragments
│  ├─ constants/
│  ├─ validation/
│  └─ types/
├─ src/
│  ├─ app/             # routes/pages
│  ├─ components/
│  ├─ hooks/
│  ├─ services/        # generated API client
│  ├─ styles/
│  └─ tests/
├─ package.json        # src/ workspace (pnpm)
├─ pyproject.toml      # bin/ package (poetry)
└─ README.md
```

**Key:** `core/schema` is the single source → `pnpm gen:types` & `poetry run gen:py` produce types for FE/BE.

**README Emoji Sections:**

* 🎯 What is CRM
* 🧱 Structure (bin/core/src)
* 🚀 Run Standalone (`prefiq serve --app app-crm`)
* 🧩 Install into Cortex
* 🔌 Extending (plugins, hooks)
* 🧪 Tests

---

### 5) **devops** (Deploy) 🚀

```
devops/
├─ docker/
│  ├─ prefiq.Dockerfile
│  ├─ cortex.Dockerfile
│  └─ app-*.Dockerfile
├─ compose/
│  └─ dev.yml
├─ helm/
│  ├─ prefiq/
│  ├─ cortex/
│  └─ app-*/
├─ terraform/
└─ README.md
```

* Images published to `ghcr.io/codexion/<name>:<version>`
* Helm values support multi-tenant modes: per-db / per-schema / RLS

---

### 6) **docs** (Site) 📘

* Docusaurus + typedoc/pdoc auto API refs
* "Try it" sandboxes linking to `examples/`
* Emoji sectioning: ✨ Features · 🛠️ Install · 🚀 Quickstart · 🧠 Concepts · 🔌 Plugins · 🧪 Testing · 📦 Releases

---

## 🔐 Security, Licensing & Governance

* **Licenses**: `prefiq` = Apache-2.0; apps default Apache-2.0 (or dual-license if you wish later)
* **SECURITY.md** in each repo; private disclosure email; CVE process stub
* **CODE\_OF\_CONDUCT.md** (Contributor Covenant)
* **CODEOWNERS** per repo; protected branches; required reviews

---

## 🛠️ Tooling & Automation

* **Reusable GH Actions** in `meta/.github/workflows`:

    * `ci-python.yml`: lint (ruff/black/mypy) → tests → build wheel → upload artifact
    * `ci-node.yml`: lint (eslint) → tests (vitest/playwright) → build → upload
    * `release.yml`: `release-please` for tag+changelog+publish (PyPI/GHCR/NPM)
* **Scaffolders** in `starters/`:

    * `create-prefiq-app` → new app (bin/core/src) with schema-driven types
    * `create-codexion-site` → new site skeleton

---

## 🧰 Developer Experience (DX)

* **pnpm workspaces** for all `src/` packages; shared tsconfig, eslint, tailwind preset from `resources`
* **poetry** for Python packages; local dev uses editable installs (`poetry install -E dev`)
* **One-command dev** per app: `pnpm dev` (FE) + `poetry run prefiq dev` (BE)
* **Hot reload** across FE/BE; OpenAPI re-generation watcher

---

## 🧪 Testing Strategy

* **Unit**: `pytest`, `vitest`
* **Contract**: OpenAPI schema checks, JSON Schema conformance
* **E2E**: Playwright (web), HTTPX + ephemeral DB containers (backend)
* **Fixtures**: seed data packs per app in `core/fixtures/`

---

## 🪜 Branching & Releases

* **Trunk-based**: `main` protected; feature branches via PR
* **Versioning**: SemVer; independent per repo
* **Tags**: `prefiq@1.2.0`, `cortex@0.8.0`, `app-crm@0.3.0`
* **Release cadence**: monthly for framework; as-needed for apps

---

## 🧾 Standard README Template (Emoji-Ready)

````md
# <Repo Name> <emoji>

> One-liner description.

## ✨ Features

- ...

## 🚀 Quickstart

```bash
# Backend
poetry install && poetry run prefiq dev
# Frontend (if applicable)
pnpm i && pnpm dev
````

## 🧱 Structure

* `bin/` – backend runtime (Python)
* `core/` – schemas, constants, validation, generated types
* `src/` – React/TS frontend

## 🔌 Integrations

* ...

## 🧪 Testing

```bash
poetry run pytest -q
pnpm test
```

## 📦 Releases & Changelog

* Automated via GitHub Actions + release-please

## 🤝 Contributing

* Conventional Commits, lint passes, tests green

## 📜 License

* Apache-2.0 (unless noted)

````

---

## ✅ First 10 Tasks (Checklist)
1. 🟢 Create org & repos: `prefiq`, `cortex`, `resources`, `app-crm`, `devops`, `docs`, `meta`
2. 🔧 Bootstrap `prefiq` (kernel, router, CLI skeleton)
3. 🧪 Wire CI for Python & Node (reusable workflows)
4. 🧱 Define `core/schema` conventions & codegen pipeline
5. 🎨 Publish `resources` (design tokens, base components, Tailwind preset)
6. 🧠 Scaffold `cortex` (auth/users/settings) + migrations
7. 🤝 Scaffold `app-crm` (bin/core/src) + first endpoints & UI page
8. 🧪 Add contract tests (OpenAPI + JSON Schema roundtrip)
9. 🚀 Dev containers & `compose/` for local run (Postgres + MinIO + Redis)
10. 📘 Docs site with “Hello Prefiq” + “Build your first app”

---

## 📍 Naming & Packages
- **Python**: `prefiq`, `cortex`, `codexion-crm`, `codexion-resources`
- **NPM**: `@codexion/crm`, `@codexion/resources`, `@codexion/erp-ui`
- **Docker**: `ghcr.io/codexion/prefiq`, `ghcr.io/codexion/cortex`, `ghcr.io/codexion/app-crm`

---

## 🔭 Optional (Future-Proofing)
- ⚙️ **Module Federation** for micro-frontends across apps
- 🧠 **AI**: standard “agent” interface in Prefiq; adapters as plugins in `app-ai`
- 🪪 **License keys** & feature flags in Cortex
- 🧩 **Marketplace**: app discovery/installation UX via Cortex

---

## 🧑‍💻 Example Commands (DX)
```bash
# Run CRM standalone (dev)
cd app-crm && poetry run prefiq dev --app bin && pnpm --filter @codexion/crm dev

# Run Cortex + CRM
# (Start API services + web clients; watch + codegen on schema change)
make dev STACK=cortex,crm
````

---

**This blueprint is ready to implement.** Next, we can scaffold `prefiq`, `cortex`, and `app-crm` with the agreed layout
and wire CI + basic dev containers. ✅
