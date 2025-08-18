# prefiq/cli/main_cli.py
import os
import typer
from typing import Optional
from prefiq.core.runtime.bootstrap import main as bootstrap_main

app = typer.Typer(help="Prefiq CLI")
server_app = typer.Typer(help="Server related commands")
app.add_typer(server_app, name="server")

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

@server_app.command("run")
def run(
    env: Optional[str] = typer.Argument(None, help="dev|prod|stage|test (default: dev)"),
    db_mode: Optional[str] = typer.Option(None, "--db-mode", help="sync|async"),
):
    normalized_env = _apply_env(env)
    if db_mode:
        os.environ["DB_MODE"] = db_mode.strip().lower()
    typer.echo(f"🚀 Booting Prefiq | ENV={normalized_env}"
               + (f" | DB_MODE={os.environ['DB_MODE']}" if "DB_MODE" in os.environ else ""))
    bootstrap_main()
    typer.echo("✅ Server bootstrapped.")

def main():  # <— add this so both 'app' and 'main' work
    app()

if __name__ == "__main__":
    main()
