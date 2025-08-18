

```
                 ┌─────────────────────────────────────────┐
                 │            Application (DI)             │
                 │  - provider_registry (auto-reg)         │
                 │  - register/boot lifecycle              │
                 │  - bind/resolve services                │
                 └───────────────┬─────────────────────────┘
                                 │
     ┌───────────────────────────┼───────────────────────────┐
     │                           │                           │
┌────▼────┐                 ┌────▼────┐                 ┌────▼────┐
│Settings │                 │Profiles │                 │ Database │
│Provider │                 │Provider │                 │ Provider │
│(binds   │                 │(binds   │                 │(binds    │
│settings)│                 │profiles)│                 │db engine)│
└────┬────┘                 └────┬────┘                 └────┬────┘
     │                           │                           │
     │                           │                           │  (validates DB cfg,
     │                           │                           │   test ping/probe,
     │                           │                           │   safe teardown)
     │                           │                           │
     │                           │                           │
     │                           │                      ┌────▼───────────────────────────┐
     │                           │                      │     Database Engine (factory)   │
     │                           │                      │  - SyncMariaDBEngine            │
     │                           │                      │  - AsyncMariaDBEngine           │
     │                           │                      └────┬────────────────────────────┘
     │                           │                           │
     │                           │                 ┌─────────▼──────────┐
     │                           │                 │  AbstractEngine     │
     │                           │                 │  (hooks, contract)  │
     │                           │                 └─────────┬──────────┘
     │                           │                           │
     │                           │               ┌───────────▼───────────┐
     │                           │               │  Cross-cutting utils   │
     │                           │               │  - retry (sync/async)  │
     │                           │               │  - pool (async)        │
     │                           │               │  - logger (queries)    │
     │                           │               │  - health (sync/async) │
     │                           │               │  - hooks (before/after)│
     │                           │               └────────────────────────┘

```

Key references: Application container + auto-registration (provider_registry) , lifecycle boot and service binding , DB provider binds engine, validates settings, checks connectivity, safe close at exit . Engines share a contract with hooks and implement sync/async with retry, logging, pooling where relevant . Query logging & slow-query flagging , health checks across sync/async .

Got it—here’s a compact, shareable package: a high-level architecture diagram, a boot sequence flow, a cleaned-up repo layout, and a concrete plan to fix the duplicate filenames.

# High-level architecture (at a glance)

```
                 ┌─────────────────────────────────────────┐
                 │            Application (DI)             │
                 │  - provider_registry (auto-reg)         │
                 │  - register/boot lifecycle              │
                 │  - bind/resolve services                │
                 └───────────────┬─────────────────────────┘
                                 │
     ┌───────────────────────────┼───────────────────────────┐
     │                           │                           │
┌────▼────┐                 ┌────▼────┐                 ┌────▼────┐
│Settings │                 │Profiles │                 │ Database │
│Provider │                 │Provider │                 │ Provider │
│(binds   │                 │(binds   │                 │(binds    │
│settings)│                 │profiles)│                 │db engine)│
└────┬────┘                 └────┬────┘                 └────┬────┘
     │                           │                           │
     │                           │                           │  (validates DB cfg,
     │                           │                           │   test ping/probe,
     │                           │                           │   safe teardown)
     │                           │                           │
     │                           │                           │
     │                           │                      ┌────▼───────────────────────────┐
     │                           │                      │     Database Engine (factory)   │
     │                           │                      │  - SyncMariaDBEngine            │
     │                           │                      │  - AsyncMariaDBEngine           │
     │                           │                      └────┬────────────────────────────┘
     │                           │                           │
     │                           │                 ┌─────────▼──────────┐
     │                           │                 │  AbstractEngine     │
     │                           │                 │  (hooks, contract)  │
     │                           │                 └─────────┬──────────┘
     │                           │                           │
     │                           │               ┌───────────▼───────────┐
     │                           │               │  Cross-cutting utils   │
     │                           │               │  - retry (sync/async)  │
     │                           │               │  - pool (async)        │
     │                           │               │  - logger (queries)    │
     │                           │               │  - health (sync/async) │
     │                           │               │  - hooks (before/after)│
     │                           │               └────────────────────────┘
```

Key references: Application container + auto-registration (provider\_registry) , lifecycle boot and service binding , DB provider binds engine, validates settings, checks connectivity, safe close at exit  . Engines share a contract with hooks  and implement sync/async with retry, logging, pooling where relevant   . Query logging & slow-query flagging , health checks across sync/async .

# Boot sequence (what happens at runtime)

1. **Configure logging & get settings** – `bootstrap.main()` initializes logging from `Settings` (level/format/namespace).
2. **Create Application & lifecycle logs** – attach `on_booting`/`on_booted` hooks.
3. **Register providers** – iterate provider list and `app.register(...)`. (Registration calls each provider’s `register`.)
4. **Boot providers** – `app.boot()` triggers booting callbacks, auto-registers any `@register_provider` classes, then boots each provider.
   * **SettingsProvider** binds `settings` (+ validates any provider’s schema\_model).
   * **ProfilesProvider** binds profiles (may derive from `settings`).
   * **DatabaseProvider** creates engine, binds as `db`, validates config, tests connectivity, registers safe teardown.
5. **Post-boot verification** – e.g., check `db` is bound.

# layout

```
prefiq/
├─ core/
│  ├─ contracts/
│  │  ├─ base_provider.py
│  └─ runtime/
│     └─ bootstrap.py
├─ providers/
│  ├─ settings_provider.py
│  ├─ profiles_provider.py
│  └─ database_provider.py
├─ database/
│  ├─ engines/
│  │  ├─ abstract_engine.py
│  │  ├─ mariadb/
│  │  │  ├─ sync_engine.py
│  │  │  ├─ async_engine.py
│  │  │  ├─ pool.py
│  │  │  ├─ retry.py
│  │  │  └─ logger.py
│  └─ driver.py
├─ settings/
│  └─ get_settings.py
└─ utils/
   └─ logger.py
```

Why this structure?

* Keeps **canonical** providers in `prefiq/providers/` (these are the ones used in production boot).
* Moves older “sample/minimal” provider implementations into a **clearly marked `legacy/`** folder under `core/contracts/providers/`.
* Keeps db engine internals under a single `database/engines/mariadb/` tree with shared `abstract_engine.py` above them.
* Separates **cross-cutting utilities** (retry, pooling, logging) into their own `utils/` folder, referenced by engines.

