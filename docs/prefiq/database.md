You’re right — providers are still effectively “hard‑wired” via `cortex.runtime.service_providers.PROVIDERS` in the current bootstrap. We already have the pieces for auto‑discovery (a metaclass‑based registry and discovery helpers), but the bootstrap isn’t using them yet. The minimal fix is to route bootstrap → discovery → registry.

Here’s a crisp plan to (1) make providers truly auto‑discovered, and (2) slim the repo by merging a few files without losing clarity.

# What’s there (and what’s off)

* The **Provider** base uses a metaclass that auto‑registers every concrete, enabled subclass at import time. That part is good: subclasses get recorded in `_PROVIDER_REGISTRY` and sorted by `.order` when you call `all_providers()`  .
* **Bootstrap** currently loops a hardcoded list `PROVIDERS` from `cortex.runtime.service_providers`, so it never asks the discovery layer for who’s installed; that’s why it feels hardcoded  .

# Clean workflow (end‑to‑end)

1. **Bootstrap (DI + discovery)**

   * Configure logging + load settings.
   * Create `Application` (the container) and attach lifecycle hooks.
   * **New step:** call `get_service_providers()` (which should call your discovery) to obtain a list of provider classes (ordered). Then `app.register(cls)` for each, then `app.boot()`.
   * Sanity log: which DB engine got bound; verify `db` exists.
     (Today bootstrap iterates a hardcoded `PROVIDERS`; we’ll switch it.)

2. **Discovery (hybrid)**

   * Based on settings: `REGISTERED_APPS`, `PROVIDER_DISCOVERY_ROOTS`, plus `PROVIDERS_INCLUDE`, `PROVIDERS_EXCLUDE`, and `PROVIDERS_ORDER`.
   * Import `apps/<app>/providers/*` + any extra roots so that the **metaclass** sees subclasses and auto‑registers them. Then collect `all_providers()`, apply exclude/order overrides, and return the sorted list.

3. **Provider lifecycle**

   * `register(app)` binds services (settings, profiles, db, migrator, …).
   * `boot(app)` does post‑bind work (hooks, warmups, ensure tables, etc.).

4. **Apps + versions**

   * `apps.cfg` remains the single source of truth for app order; app scaffolder writes a provider stub and a first migration on `new_app`.

5. **Base app: cortex**

   * Cortex ships providers like `AuthProvider`, `TenancyProvider`, `UiProvider`, etc. They’re discovered like any other app provider.

# Repo simplification (fewer files, same power)

**Goal:** keep each concept discoverable, but remove duplication and merge thin wrappers.

1. **Unify provider base types**

* Merge `prefiq/core/contracts/base_provider.py` (**Application**, **BaseProvider**) and `prefiq/core/provider.py` (**Provider** with auto‑registry) into:

  * `prefiq/core/application.py` (Application container)
  * `prefiq/core/provider.py` (one base with metaclass + typed hooks)
* Why: today there are two “provider bases” with different names; this confuses authors. One clear base + one container is enough (and keeps discovery simple).

2. **Collapse discovery façades**

* Merge `service_providers.py` and `discover_provider.py` into:

  * `prefiq/core/discovery.py` with a single `discover_providers()` and (optionally) a thin `get_service_providers()` alias.
* Then **bootstrap imports from here** instead of `cortex.runtime.service_providers`.

3. **Trim doctors**

* Keep a single `prefiq/cli/doctor.py` module that defines `doctor boot|database|migrate` subcommands in one file (the functions can still import lazy/heavy pieces inside the command bodies). This removes three tiny files with nearly identical structure.

4. **CLI consolidation**

* Keep `main_cli.py` as the single Typer entrypoint (good), but move the tiny “builder” CLI wrappers directly under `prefiq/cli/apps.py` to avoid `cli/apps/builder.py` + `apps/app_builder.py` *and* keep `apps/app_builder.py` (which is real logic) as is.

5. **Config providers**

* Optional: merge `ConfigProvider` and `ProfilesProvider` into a single `ConfigProvider` (two small files → one). It can bind `settings` then derive and bind `profiles` in one place.

6. **Bootstrap duplication**

* There appear to be duplicate bootstraps; keep **one** at `prefiq/core/runtime/bootstrap.py`. Remove the duplicate if present elsewhere (same content).

# “Ready to develop” (dev env)

* `prefiq boot dev` (CLI) should: configure logging, run discovery, register/boot, show provider list + migrations table check, then start your dev server or shell.
* DB: `DatabaseProvider` binds the engine and sets hooks; `MigrationProvider` ensures the meta table and binds a `migrator`.
* App tooling: `prefiq app new|drop|reinstall` remains as is.

# Target repo layout (after slimming)

```
prefiq/
  core/
    application.py            # Application container (merged)
    provider.py               # Provider base + metaclass registry (merged)
    discovery.py              # discover_providers() + helpers (merged)
    runtime/
      bootstrap.py            # single bootstrap using discovery
  providers/
    database_provider.py
    migration_provider.py
    config_provider.py        # (merged settings+profiles)  ← optional merge
  apps/
    app_builder.py            # logic (keep)
    app_scaffold.py
    app_stubs.py
    app_cfg.py
  cli/
    main.py                   # (moved from main_cli.py)
    doctor.py                 # (merged boot/database/migration doctor)
    apps.py                   # (builder CLI moved here)
  settings/get_settings.py
```

# Concrete changes (wire‑up)

1. **Change bootstrap to discovery**

   * Replace:

     ```py
     from cortex.runtime.service_providers import PROVIDERS
     ...
     for provider in PROVIDERS:
         app.register(provider)
     ```

     with:

     ```py
     from prefiq.core.discovery import discover_providers
     for provider in discover_providers():
         app.register(provider)
     ```
   * This eliminates the hardcoded list and uses the metaclass registry once discovery has imported provider modules. (The current bootstrap’s hardcoded import is what causes your “only connected via hardcoded” issue  ; the metaclass registry is otherwise sound .)

2. **Ensure discovery imports provider modules**

   * Discovery should import `apps/<app>/providers/*` for each app in settings (or `apps.cfg`), plus any extra roots, then read `all_providers()` and apply include/exclude/order overrides. (Your metaclass needs those imports to populate the registry.)

3. **Provider base unification**

   * Keep one base class named `Provider` with `register(self, app)` and `boot(self, app)` (the current metaclass base already defines this signature and sorts by `.order`  ).
   * Keep `Application` (container) separate and lightweight.

4. **Optional merges**

   * Merge settings+profiles providers into one `ConfigProvider`.
   * Merge doctor commands into one module.

# To‑Do list (ordered)

1. **Refactor bootstrap to use discovery** (remove dependency on `cortex.runtime.service_providers.PROVIDERS`).
2. **Create `prefiq/core/discovery.py`** (move/merge existing discovery helpers; import apps’ providers; return sorted classes).
3. **Unify provider bases** into `core/application.py` + `core/provider.py`; adapt imports in providers.
4. **(Optional) Merge `ConfigProvider` + `ProfilesProvider` → `ConfigProvider`.**
5. **(Optional) Merge doctor modules into one `doctor.py`** with subcommands.
6. **Rename `main_cli.py` → `cli/main.py` and mount subcommands lazily** (as you already do).
7. **Delete duplicates** (extra bootstrap, thin wrappers superseded by merges).
8. **Smoke test**: `prefiq doctor boot` → expect “Application booted”; `prefiq doctor database --verbose`; `prefiq run migrate` via bound migrator.
9. **Scaffold cortex** (if not already) and verify cortex providers are discovered and ordered correctly.

---

If you’re happy with this plan, say **“code”**, and I’ll implement it in this order:

1. Update **bootstrap** to call discovery.
2. Add **core/discovery.py** with import‑and‑collect logic.
3. Unify **application/provider** bases and fix imports.
4. (If you want) merge **Settings+Profiles** and **doctor** files.

I’ll keep any deletions/renames surgical and note them in a short diff summary.
