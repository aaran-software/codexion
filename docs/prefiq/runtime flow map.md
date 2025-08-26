awesome — here’s the **runtime flow map** of your stack, step-by-step, with where each concern plugs in. no code yet.

# 1) Process starts

* **CLI** (`python -m prefiq.main`): Typer mounts only the command groups you invoke (e.g. `doctor`, `app`, `provider`, `run migrate`). This keeps startup light.
* **Server / custom entry**: you typically call a bootstrap that builds the App container, registers providers, then boots.

# 2) Settings load (once, cached)

* `.env` (or env vars) → Pydantic Settings object.
* Normalization happens here (engine aliases like `postgresql→postgres`, default ports, log level, etc).
* Anything that later asks for settings gets the same cached object unless you explicitly clear/refresh.

# 3) Provider discovery

* Two sources are merged:

  1. **Hardcoded core** providers (e.g., Config → Database → Migration).
  2. **Discovered** providers from:

     * `REGISTERED_APPS` (env) and **apps declared in `config/apps.cfg`**
     * additional discovery roots (if any).
* Optional include/exclude/order overrides are applied.
* Output: an ordered list of provider classes.

# 4) Application container builds & registers providers

* A singleton **Application** (service container) is created.
* For each provider class:

  * Construct provider (passing the app).
  * Call **`register()`**: bind services, singletons, repos, routers, etc.
* App stores provider instances and bound services by key.

# 5) Boot phase

* App calls **`boot()`** on each provider in order:

  * Late wiring happens here: route mounting, pool warmups, event hooks, cron wiring.
  * If a provider needs something another provider published, this phase safely sees it.

# 6) Database engine availability

* A **default engine** singleton is created lazily the first time something asks for it (based on current settings).
* You can also create **named engines** (e.g., `DEV`, `ANALYTICS`) that live side-by-side; these read `DEV_DB_*` / `ANALYTICS_DB_*` envs and keep separate connections.

# 7) Using the database (repositories/services)

* Callers don’t touch engines directly; they go via a **ConnectionManager**:

  * **Sync**: `with connection_manager.transaction(): ...`
  * **Async**: `async with connection_manager.transaction_async(): ...`
* The manager will:

  * choose the correct engine (default or a **named** one),
  * run a **transaction** via the engine’s native CM or emulate with begin/commit/rollback,
  * handle env scoping for named engines so settings are correct during operations.

# 8) HTTP/API delivery (when used)

* A provider (or your bootstrap) mounts **FastAPI routers** as inbound adapters.
* Controllers (endpoints) are thin: parse/validate input → call **Application Service** (use case) → return a response DTO (view).
* Services call **Repositories** (outbound adapters) which use the **ConnectionManager** to execute SQL (or ORM).

# 9) CLI tools (operational)

* **doctor**:

  * Boot diagnostics: load settings → discover providers → register → boot.
  * Database diagnostics: show engine, DSN (masked), run `SELECT 1`, print pool stats if supported.
  * Profile sweep: can test `DEFAULT`, `DEV`, `ANALYTICS` by temporarily patching env and rebuilding engines.
* **app**: scaffolds app folders, registers them in `config/apps.cfg`.
* **provider**: lists discovered providers with order and module info.
* **run migrate / sanity / clear-cache**: operational helpers (migration runner, quick checks, cache reset).

---

## where your Project Manager module fits

* **Boundaries** (Clean/Hex + DDD-lite):

  * **domain/**: `Project`, `Task`, value objects (e.g., `TaskTitle`), domain errors, policies.
  * **application/**: use cases (`CreateTask`, `ListTasks`, `ChangeStatus`), **ports** (`ProjectRepo`, `TaskRepo`, `TenantContext`, `Clock`).
  * **adapters/inbound/**: HTTP controllers (FastAPI endpoints) → map HTTP DTOs ↔ use case DTOs.
  * **adapters/outbound/**: SQL repositories implementing ports; they use the ConnectionManager (default or tenant-named engine).
  * **infrastructure/**: provider that binds repos to ports, mounts routes, and wires tenant resolution.
* **Simple CRUD** pieces (e.g., list projects) can be **Service + Repo** only (lighter ceremony) inside the same module. Complex flows (reviews, SLA checks, notifications, multi-tenant isolation) live in **Clean/Hex** layers.

---

## request/response walkthrough (example)

1. **HTTP POST** `/api/tasks` → Controller validates request DTO.
2. Controller calls **`CreateTask.handle(input)`** in the **application** layer.
3. Use case:

   * `ProjectRepo.get(project_id)` to ensure project exists.
   * Construct `Task` domain object (value objects validate rules).
   * `TaskRepo.create(task)` to persist via **ConnectionManager** (transactional).
4. Use case returns an **output DTO** (id, timestamps).
5. Controller returns **201** with the response DTO.

**Tenancy:** a middleware/inbound adapter sets **TenantContext** (from header/subdomain). Outbound adapters (repos) use it to pick the right **named engine** or schema — the **domain** and use cases stay tenant-agnostic.

---

## mental checklist when adding new features

* Is it just CRUD? → Service + Repo (fast).
* Any non-trivial rules, workflows, events, or tenancy? → put rules in **domain**, orchestrate with **use cases**, talk to infra via **ports**.
* Need read optimization or dashboards? → consider a read-optimized query service (no need to jump to full CQRS unless real pain).
* Will this run in multiple DBs? → add a **named engine** and select it via TenantContext or feature flag.

---

If this looks right, say **“code next: clean+hex base”** (or **“code next: service+repo slice”**) and tell me which project entities you want first (Projects, Tasks, Comments, Attachments, etc.). I’ll scaffold only that, wired to your existing engine and provider system.
