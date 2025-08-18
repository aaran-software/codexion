# prefiq/cli/cortex/server.py

import typer
import subprocess
import os

server_cmd = typer.Typer(help="Prefiq CLI tool")

def run_command(cmd: str):
    print(f"[~] Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

@server_cmd.command()
def run(mode: str = typer.Argument(..., help="Mode: dev or prod")):
    """
    Run backend and frontend servers.

    Examples:
      prefiq server dev
      prefiq server prod
    """
    mode = mode.lower()

    if mode not in ["dev", "prod"]:
        typer.echo("[!] Mode must be 'dev' or 'prod'")
        raise typer.Exit(code=1)

    os.environ["MODE"] = mode

    if mode == "prod":
        print("[+] Building frontend for production...")
        run_command("npm run build")

        print("[🚀] Starting FastAPI backend in production...")
        run_command("gunicorn cortex.main:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:5005 -w 4 --timeout 60")
    else:
        print("[🚀] Starting backend and frontend in development...")
        run_command(
            'concurrently "uvicorn cortex.main:app --host 0.0.0.0 --port 5005 --reload" '
            '"npm run dev -- --host 0.0.0.0 --port 3005"'
        )
