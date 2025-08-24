# prefiq/cli/utils/tools.py
from __future__ import annotations

import os
import shutil
from pathlib import Path
import typer

# Updated imports to match your refactor
from prefiq.core.bootstrap import main as bootstrap_main
from prefiq.core.application import Application
from prefiq.settings.get_settings import load_settings


def _maybe_await(x):
    """Return awaited value if x is awaitable, else x."""
    try:
        import inspect
        if inspect.isawaitable(x):
            import asyncio
            return asyncio.run(x)
    except Exception:
        pass
    return x


def sanity() -> None:
    """
    Run a quick sanity checklist:
      - Boot providers (via unified bootstrap)
      - Settings loaded
      - DB connectivity (handles sync/async engines)
    """
    typer.echo("🩺 Running sanity checklist...")

    # Unified boot (idempotent for your Application singleton pattern)
    bootstrap_main()

    app = Application.get_app()

    # Settings
    s = load_settings()
    typer.echo(f"✅ Settings loaded: ENV={getattr(s, 'ENV', 'development')}")

    # DB connectivity
    db = app.resolve("db")
    if not db:
        typer.echo("❌ No 'db' binding found in the container.")
        raise typer.Exit(code=1)

    ok = True
    try:
        test = getattr(db, "test_connection", None)
        if callable(test):
            ok = _maybe_await(test())
        else:
            # Fallback: try a lightweight "SELECT 1" if the engine exposes helpers
            scalar = getattr(db, "scalar", None) or getattr(db, "fetch_value", None)
            if callable(scalar):
                val = _maybe_await(scalar("SELECT 1"))
                ok = str(val) == "1" or val is True
    except Exception:
        ok = False

    if not ok:
        typer.echo("❌ DB connectivity FAILED")
        raise typer.Exit(code=1)

    typer.echo("✅ DB connectivity OK")


def clear_cache(path: str = ".") -> None:
    """
    Remove all __pycache__ directories and .pyc/.pyo files recursively.
    """
    root = Path(path).resolve()
    typer.echo(f"🧹 Clearing Python caches under {root} ...")
    removed_dirs = 0
    removed_files = 0

    for r, dirs, files in os.walk(root):
        # remove __pycache__ dirs
        for d in list(dirs):
            if d == "__pycache__":
                shutil.rmtree(Path(r) / d, ignore_errors=True)
                removed_dirs += 1
        # remove .pyc/.pyo files
        for f in files:
            if f.endswith(".pyc") or f.endswith(".pyo"):
                try:
                    Path(r, f).unlink()
                    removed_files += 1
                except OSError:
                    pass

    typer.echo(f"✅ Removed {removed_dirs} __pycache__/ and {removed_files} .pyc/.pyo")
