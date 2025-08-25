# prefiq/cli/core/server.py
from __future__ import annotations

import os
import sys
import signal
import platform
import subprocess
from pathlib import Path
from typing import Optional

import typer
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from prefiq.core.bootstrap import main as bootstrap_main
from prefiq.core.application import Application
from prefiq.core.logger import okc, failx
from prefiq.settings.get_settings import load_settings

server_app = typer.Typer(help="Run/Manage the Prefiq HTTP server")

# --------------------------------------------------------------------------------------------------
# env helpers
# --------------------------------------------------------------------------------------------------

_ENV_ALIAS = {"dev": "development", "development":"development",
              "live":"production","prod":"production","production":"production",
              "stage":"staging","staging":"staging","test":"test","testing":"test"}

def _apply_env(alias: str | None) -> str:
    norm = _ENV_ALIAS.get((alias or "dev").lower(), "development")
    os.environ["ENV"] = norm
    return norm

def _as_bool(v, default=False) -> bool:
    if isinstance(v, bool):
        return v
    s = (str(v) if v is not None else "").strip().lower()
    if s in {"1", "true", "yes", "y", "on"}:
        return True
    if s in {"0", "false", "no", "n", "off"}:
        return False
    return default

def _as_int(v, default: int) -> int:
    try:
        return int(v)
    except (ValueError, TypeError):
        return default

def _env_default(key: str, default=None):
    s = load_settings()
    return getattr(s, key, default)

# --------------------------------------------------------------------------------------------------
# config resolution (from .env with CLI overrides)
# --------------------------------------------------------------------------------------------------

def _resolve_server_config(
    host: str | None,
    port: int | None,
    https: bool | None,
    certfile: str | None,
    keyfile: str | None,
    reload_flag: bool | None,
    workers: int | None,
):
    s = load_settings()
    default_host_by_env = "127.0.0.1" if getattr(s, "ENV", "development") == "development" else "0.0.0.0"

    d_host = _env_default("SERVER_HOST", default_host_by_env)
    d_port = _as_int(_env_default("SERVER_PORT", 5001), 5001)
    d_https = _as_bool(_env_default("SERVER_HTTPS", False), False)
    d_cert  = _env_default("SERVER_CERTFILE", None)
    d_key   = _env_default("SERVER_KEYFILE", None)
    d_reload  = _as_bool(_env_default("SERVER_RELOAD", False), False)
    d_workers = _as_int(_env_default("SERVER_WORKERS", 1), 1)

    return {
        "host": host or d_host,
        "port": port or d_port,
        "https": d_https if https is None else https,
        "certfile": certfile or d_cert,
        "keyfile": keyfile or d_key,
        "reload": d_reload if reload_flag is None else d_reload,
        "workers": workers or d_workers,
    }

# --------------------------------------------------------------------------------------------------
# ASGI factory
# --------------------------------------------------------------------------------------------------

def build_asgi():
    """
    Factory target for uvicorn: `uvicorn prefiq.cli.core.server:build_asgi --factory`
    Ensures providers are bootstrapped, then returns FastAPI app bound at "http.app".
    """
    bootstrap_main()
    app = Application.get_app().resolve("http.app")
    if app is None:
        raise RuntimeError("No HTTP app bound. Did your Providers mount routes?")

    # ---- extra middleware & default routes ----
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/favicon.ico", include_in_schema=False)
    def favicon():
        icon_path = Path(__file__).parent / "assets" / "images" / "favicon.svg"
        return FileResponse(icon_path)

    @app.get("/")
    def root():
        return {"status": "running"}

    return app

# --------------------------------------------------------------------------------------------------
# foreground runner
# --------------------------------------------------------------------------------------------------

def _run_foreground(cfg: dict) -> None:
    bootstrap_main()
    app = Application.get_app().resolve("http.app")
    if app is None:
        typer.echo(failx("❌ No HTTP app bound. Did your Providers mount routes?"))
        raise typer.Exit(code=1)

    scheme = "https" if cfg["https"] else "http"
    typer.echo(okc(f"🌐 Starting server on {scheme}://{cfg['host']}:{cfg['port']}  "
                   f"(reload={'on' if cfg['reload'] else 'off'}, workers={cfg['workers']})"))

    uvicorn.run(
        app,
        host=cfg["host"],
        port=cfg["port"],
        reload=cfg["reload"],
        workers=cfg["workers"],
        ssl_certfile=cfg["certfile"] if cfg["https"] else None,
        ssl_keyfile=cfg["keyfile"] if cfg["https"] else None,
    )

# --------------------------------------------------------------------------------------------------
# daemon (background) management
# --------------------------------------------------------------------------------------------------

def _runtime_paths() -> tuple[Path, Path]:
    root = Path(load_settings().project_root)
    run_dir = (root / ".prefiq").resolve()
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir / "server.pid", run_dir / "server.log"

def _is_running(pid: int) -> bool:
    try:
        if platform.system() == "Windows":
            # On Windows, os.kill with 0 works on 3.2+, but tasklist is more explicit
            out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}"], capture_output=True, text=True)
            return str(pid) in out.stdout
        else:
            os.kill(pid, 0)
            return True
    except (ValueError, TypeError):
        return False

def _read_pid() -> Optional[int]:
    pid_file, _ = _runtime_paths()
    try:
        pid = int(pid_file.read_text().strip())
        return pid if _is_running(pid) else None
    except (ValueError, TypeError):
        return None

def _write_pid(pid: int) -> None:
    pid_file, _ = _runtime_paths()
    pid_file.write_text(str(pid), encoding="utf-8")

def _clear_pid() -> None:
    pid_file, _ = _runtime_paths()
    try: pid_file.unlink(missing_ok=True)  # py3.8+: catch FileNotFoundError if needed
    except (ValueError, TypeError): pass

def _start_daemon(cfg: dict) -> None:
    # Build uvicorn cmd using factory so the child can bootstrap itself
    scheme = "https" if cfg["https"] else "http"
    args = [
        sys.executable, "-m", "uvicorn",
        "prefiq.cli.core.server:build_asgi", "--factory",
        "--host", str(cfg["host"]),
        "--port", str(cfg["port"]),
        "--workers", str(cfg["workers"]),
    ]
    if cfg["reload"]:
        args.append("--reload")
    if cfg["https"]:
        if not cfg["certfile"] or not cfg["keyfile"]:
            typer.echo(failx("❌ SERVER_CERTFILE and SERVER_KEYFILE (or flags) are required for HTTPS"))
            raise typer.Exit(code=1)
        args += ["--ssl-certfile", cfg["certfile"], "--ssl-keyfile", cfg["keyfile"]]

    _, log_path = _runtime_paths()
    log_f = open(log_path, "a", encoding="utf-8")
    # Inherit current env (includes ENV we just set)
    proc = subprocess.Popen(args, stdout=log_f, stderr=log_f, stdin=subprocess.DEVNULL)
    _write_pid(proc.pid)
    typer.echo(okc(f"🟢 Server started in background at {scheme}://{cfg['host']}:{cfg['port']}  (PID {proc.pid})"))
    typer.echo(f"(Logs: {log_path})")

def _stop_daemon() -> None:
    pid = _read_pid()
    if not pid:
        typer.echo("Server is not running.")
        return
    try:
        if platform.system() == "Windows":
            subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], check=False)
        else:
            os.kill(pid, signal.SIGTERM)
    except Exception as e:
        typer.echo(failx(f"❌ Failed to stop PID {pid}: {e}"))
        raise typer.Exit(code=1)
    else:
        _clear_pid()
        typer.echo(okc(f"🔴 Server stopped (PID {pid})."))

# --------------------------------------------------------------------------------------------------
# Commands
# --------------------------------------------------------------------------------------------------

@server_app.command("run")
def run_alias(
    env: str | None = typer.Argument(None, help="dev|live|stage|test (default: dev)"),
    host: str | None = typer.Option(None, "--host", help="Host to bind (overrides .env)"),
    port: int | None = typer.Option(None, "--port", help="Port to bind (overrides .env)"),
    https: bool | None = typer.Option(None, "--https", help="Enable HTTPS"),
    certfile: str | None = typer.Option(None, "--certfile", help="Path to SSL cert"),
    keyfile: str | None = typer.Option(None, "--keyfile", help="Path to SSL key"),
    reload: bool | None = typer.Option(None, "--reload", help="Auto-reload on code changes"),
    workers: int | None = typer.Option(None, "--workers", help="Number of worker processes"),
):
    normalized_env = _apply_env(env)
    typer.echo(f"🚀 Booting Prefiq | ENV={normalized_env}")
    cfg = _resolve_server_config(host, port, https, certfile, keyfile, reload, workers)
    _run_foreground(cfg)

@server_app.command("start")
def cmd_start(
    env: Optional[str] = typer.Argument(None, help="dev|live|stage|test (default: dev)"),
    host: str | None = typer.Option(None, "--host", help="Override host"),
    port: int | None = typer.Option(None, "--port", help="Override port"),
    https: bool | None = typer.Option(None, "--https", help="Enable HTTPS"),
    certfile: str | None = typer.Option(None, "--certfile", help="Path to SSL cert"),
    keyfile: str | None = typer.Option(None, "--keyfile", help="Path to SSL key"),
    reload: bool | None = typer.Option(None, "--reload", help="Auto-reload on code changes"),
    workers: int | None = typer.Option(None, "--workers", help="Number of worker processes"),
):
    normalized_env = _apply_env(env)
    typer.echo(f"🚀 Starting Prefiq (daemon) | ENV={normalized_env}")
    if _read_pid():
        typer.echo("Server already running.")
        raise typer.Exit(code=0)
    cfg = _resolve_server_config(host, port, https, certfile, keyfile, reload, workers)
    _start_daemon(cfg)

@server_app.command("stop")
def cmd_stop():
    _stop_daemon()

@server_app.command("restart")
def cmd_restart(
    env: Optional[str] = typer.Argument(None, help="dev|live|stage|test (default: dev)"),
    host: str | None = typer.Option(None, "--host", help="Override host"),
    port: int | None = typer.Option(None, "--port", help="Override port"),
    https: bool | None = typer.Option(None, "--https", help="Enable HTTPS"),
    certfile: str | None = typer.Option(None, "--certfile", help="Path to SSL cert"),
    keyfile: str | None = typer.Option(None, "--keyfile", help="Path to SSL key"),
    reload: bool | None = typer.Option(None, "--reload", help="Auto-reload on code changes"),
    workers: int | None = typer.Option(None, "--workers", help="Number of worker processes"),
):
    normalized_env = _apply_env(env)
    typer.echo(f"🔄 Restarting Prefiq (daemon) | ENV={normalized_env}")
    _stop_daemon()
    cfg = _resolve_server_config(host, port, https, certfile, keyfile, reload, workers)
    _start_daemon(cfg)
