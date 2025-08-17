perfect — here’s a clean, step-by-step **to-do plan** grouped by **P0 → P2**. after this, tell me “start with P0-1” (or any task id) and we’ll tackle it together, one bite at a time.

---

# P0 — Foundations (merge blockers)

**P0-1. Namespace & provider wiring**

* Unify on `prefiq.*` (remove any `cortex.*` imports).
* Single provider registry; bootstrap uses it.
* [✅] DoD: `python -m prefiq.core.runtime.bootstrap` boots with providers and no import errors.

**P0-2. Engine selection sanity**

* Default `DB_ENGINE` to `mariadb` (or map `mysql → mariadb`).
* Limit resolver to engines that actually exist today (MariaDB).
* [] DoD: `db.test_connection()` passes using env defaults.

**P0-3. DatabaseProvider → unified driver**

* DatabaseProvider binds `db` via a single resolver (no hidden globals).
* [] DoD: `app.resolve("db")` returns the same instance used in health checks.

**P0-4. Async retry correctness**

* Ensure async engine uses `with_retry_async` (not sync retry).
* [] DoD: an intentionally flaky query is retried asynchronously (observed in logs).

**P0-5. Async transactions**

* Add `async with db.transaction():` that pins one pooled connection across statements (begin/commit/rollback).
* [] DoD: a two-statement transaction commits atomically; rollback works on exception.

**P0-6. Sync test\_connection guard**

* Validate/open connection before cursor usage.
* [] DoD: `db.test_connection()` succeeds right after boot; handles down DB gracefully (returns False).

**P0-7. Provider config validation**

* Give `DatabaseProvider` a `schema_namespace="database"` and a Pydantic `schema_model`.
* `SettingsProvider` fails fast on invalid env.
* [] DoD: bad env → boot aborts with clear validation errors.

---

# P1 — Developer experience & observability

**P1-1. Boot-time async pool init**

* Explicitly initialize async pool on app boot when `DB_MODE=async`.
* [] DoD: first query does not incur pool warm-up cost; startup fails early if misconfigured.

**P1-2. Structured logging**

* Replace prints with structured logs (level, duration, query size, retries, txn id).
* [] DoD: slow queries (>N ms) are clearly logged with timings & retry counts.

**P1-3. Health endpoint**

* Wire `is_healthy(db)` into `/healthz`; add to boot logs.
* [] DoD: `/healthz` returns 200 when DB ok; 503 with reason when not.

**P1-4. Hook presets**

* Ship default before/after hooks (timing, masking params) + simple API to register custom hooks.
* [] DoD: sample app registers a custom hook without touching engine code.

**P1-5. Docs: “DB Usage”**

* Quick guide: resolve `db`, run queries, use transactions (sync/async), per-request overrides, hooks.
* [] DoD: README section with runnable snippets.

**P1-6. Sample queries**

* Add minimal repo “examples/” showing sync and async flows against a local MariaDB/SQLite.
* [] DoD: `make run-sync-example` and `make run-async-example` both succeed.

---

# P2 — Expansion & polish

**P2-1. Postgres engine**

* Implement `SyncPostgresEngine` (and async if needed) using the same `AbstractEngine` contract.
* [] DoD: `DB_ENGINE=postgres` boots; basic CRUD + transactions pass.

**P2-2. SQLite engine (dev/test)**

* Lightweight sync engine; optional async wrapper.
* [] DoD: `DB_ENGINE=sqlite` runs examples; great for CI.

**P2-3. MongoDB adapter (optional)**

* Provide a thin adapter matching the contract semantics (no SQL).
* [] DoD: basic CRUD semantics mapped; health check works.

**P2-4. Connection leak detection**

* Track connection acquire/release; warn on leaked cursors/conns.
* [] DoD: intentional leak triggers a warning with stack origin.

**P2-5. Metrics**

* Emit counters/histograms: queries, retries, errors, latency, pool size.
* [] DoD: metrics visible via logs or a pluggable exporter.

**P2-6. Config normalizers**

* Normalize env (case-insensitive booleans, engine aliases).
* [] DoD: messy env still produces valid, typed config.

**P2-7. Integration tests (CI)**

* Matrix for engines (mariadb, postgres, sqlite) and modes (sync/async).
* [] DoD: green CI; dockerized DBs come up, tests run & tear down.

**P2-8. Migration story (optional)**

* Document how to layer Alembic (SQL) or framework-native migrations.
* [] DoD: one example migration applied across engines that support it.

---

want to go step-by-step? say **“start with P0-1”** (or any task id above). I’ll execute that task next and show you exactly what changed, with tiny diff-style snippets and a quick test run.


P0-1 ✅ providers wired (app-owned registry)

P0-2 ✅ strict mariadb + no double-registration + async-safe provider boot

P0-4 ✅ async engine uses with_retry_async and runs all driver calls in a thread

po-5 ✅ async transactions with pooled connections

po-6 ✅ sync test_connection guard