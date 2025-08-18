# prefiq/cli/utils/tools.py
import os, shutil
from pathlib import Path
import typer

from prefiq.core.runtime.bootstrap import main as bootstrap_main
from prefiq.core.contracts.base_provider import Application
from prefiq.settings.get_settings import load_settings

def sanity():
    """
    Run a quick sanity checklist:
      - Boot providers
      - Settings loaded
      - DB connectivity
    """
    typer.echo("🩺 Running sanity checklist...")
    bootstrap_main()
    app = Application.get_app()

    s = load_settings()
    typer.echo(f"✅ Settings loaded: ENV={getattr(s, 'ENV', 'development')}")

    db = app.resolve("db")
    if not db:
        raise typer.Exit(code=1)
    ok = db.test_connection()
    if hasattr(ok, "__await__"):
        import asyncio
        ok = asyncio.run(ok)
    if not ok:
        typer.echo("❌ DB connectivity FAILED")
        raise typer.Exit(code=1)
    typer.echo("✅ DB connectivity OK")

def clear_cache(path: str = "."):
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
