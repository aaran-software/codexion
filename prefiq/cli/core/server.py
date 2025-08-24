# prefiq/cli/core/server.py
from __future__ import annotations
import os
from typing import Optional
import typer
from prefiq.core.bootstrap import main as bootstrap_main

server_app = typer.Typer(help="Server related commands")

def _apply_env(env_alias: Optional[str]) -> str:
    alias = (env_alias or "dev").strip().lower()
    mapping = {
        "dev": "development", "development": "development",
        "prod": "production", "production": "production",
        "stage": "staging", "staging": "staging",
        "test": "test", "testing": "test",
    }
    normalized = mapping.get(alias, alias or "development")
    os.environ["ENV"] = normalized
    return normalized

@server_app.command("run")  # <-- was "server"
def run(
    env: Optional[str] = typer.Argument(None, help="dev|prod|stage|test (default: dev)"),
    db_mode: Optional[str] = typer.Option(None, "--db-mode", help="sync|async"),
):
    normalized_env = _apply_env(env)
    if db_mode:
        os.environ["DB_MODE"] = db_mode.strip().lower()

    typer.echo(
        f"🚀 Booting Prefiq | ENV={normalized_env}"
        + (f" | DB_MODE={os.environ['DB_MODE']}" if "DB_MODE" in os.environ else "")
    )
    bootstrap_main()
    typer.echo("✅ Server bootstrapped.")
