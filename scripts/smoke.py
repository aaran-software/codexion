"""
Lightweight end-to-end smoke:
- boots the app
- checks DI bindings (settings, profiles, db)
- runs SELECT 1
- prints engine info + health
"""

import inspect
import asyncio

from prefiq.core.runtime.bootstrap import main
from prefiq.core.contracts.base_provider import Application

def maybe_run(awaitable_or_value):
    if inspect.isawaitable(awaitable_or_value):
        return asyncio.run(awaitable_or_value)
    return awaitable_or_value

def fail(msg):
    print(f"[SMOKE] FAIL: {msg}")
    raise SystemExit(1)

def ok(msg):
    print(f"[SMOKE] OK: {msg}")

def run():
    # boot
    main()
    app = Application.get_app()

    # bindings
    settings = app.resolve("settings")
    profiles = app.resolve("profiles")
    db = app.resolve("db")
    if not settings: fail("settings not bound")
    if not profiles: fail("profiles not bound")
    if not db: fail("db not bound")
    ok("bindings present (settings, profiles, db)")

    # engine info
    engine_type = type(db).__name__
    print(f"[SMOKE] Engine: {engine_type}")

    # health (works for sync/async)
    # use the engine's own test_connection; no extra imports required
    healthy = bool(maybe_run(db.test_connection()))
    if not healthy:
        fail("db.test_connection() returned False")
    ok("db.test_connection()")

    # simple query
    row = maybe_run(db.fetchone("SELECT 1"))
    if not row:
        fail("SELECT 1 returned no row")
    print(f"[SMOKE] SELECT 1 -> {row}")
    ok("query path works")

    print("[SMOKE] All good ✅")

if __name__ == "__main__":
    run()
