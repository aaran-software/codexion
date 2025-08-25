# prefiq/cli/core/server.py
from __future__ import annotations

import typer
import uvicorn

from prefiq.core.application import Application
from prefiq.core.logger import okc, failx
from prefiq.settings.get_settings import load_settings

server_app = typer.Typer(help="Run HTTP/HTTPS server")


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
    except Exception:
        return default


def _env_default(key: str, default=None):
    """
    Read from Settings (extra='allow' means unknown keys still appear).
    """
    s = load_settings()
    return getattr(s, key, default)


def _resolve_server_config(
    host: str | None,
    port: int | None,
    https: bool | None,
    certfile: str | None,
    keyfile: str | None,
    reload_flag: bool | None,
    workers: int | None,
):
    # Defaults from .env (or sensible fallbacks)
    d_host = _env_default("SERVER_HOST", "0.0.0.0")
    d_port = _as_int(_env_default("SERVER_PORT", 5001), 5001)

    d_https = _as_bool(_env_default("SERVER_HTTPS", False), False)
    d_cert = _env_default("SERVER_CERTFILE", None)
    d_key = _env_default("SERVER_KEYFILE", None)

    d_reload = _as_bool(_env_default("SERVER_RELOAD", False), False)
    d_workers = _as_int(_env_default("SERVER_WORKERS", 1), 1)

    return {
        "host": host or d_host,
        "port": port or d_port,
        "https": d_https if https is None else https,
        "certfile": certfile or d_cert,
        "keyfile": keyfile or d_key,
        "reload": d_reload if reload_flag is None else reload_flag,
        "workers": workers or d_workers,
    }


def _start(
    host: str | None,
    port: int | None,
    https: bool,
    certfile: str | None,
    keyfile: str | None,
    reload_flag: bool,
    workers: int,
) -> None:
    app = Application.get_app().resolve("http.app")
    if app is None:
        typer.echo(failx("❌ No HTTP app bound. Did you mount routes via a Provider?"))
        raise typer.Exit(code=1)

    if https and (not certfile or not keyfile):
        typer.echo(failx("❌ --certfile and --keyfile required for HTTPS"))
        raise typer.Exit(code=1)

    scheme = "https" if https else "http"
    typer.echo(okc(f"🌐 Starting server on {scheme}://{host}:{port}  "
                   f"(reload={'on' if reload_flag else 'off'}, workers={workers})"))

    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=reload_flag,
        workers=workers,
        ssl_certfile=certfile if https else None,
        ssl_keyfile=keyfile if https else None,
    )


@server_app.command("start")
def start(
    host: str | None = typer.Option(None, "--host", help="Host to bind (overrides .env)"),
    port: int | None = typer.Option(None, "--port", help="Port to bind (overrides .env)"),
    https: bool | None = typer.Option(None, "--https", help="Enable HTTPS"),
    certfile: str | None = typer.Option(None, "--certfile", help="Path to SSL cert"),
    keyfile: str | None = typer.Option(None, "--keyfile", help="Path to SSL key"),
    reload: bool | None = typer.Option(None, "--reload", help="Auto-reload on code changes"),
    workers: int | None = typer.Option(None, "--workers", help="Number of worker processes"),
):
    cfg = _resolve_server_config(host, port, https, certfile, keyfile, reload, workers)
    _start(**cfg)


# Backwards-compat alias (`prefiq server run`)
@server_app.command("run")
def run_alias(
    host: str | None = typer.Option(None, "--host", help="Host to bind (overrides .env)"),
    port: int | None = typer.Option(None, "--port", help="Port to bind (overrides .env)"),
    https: bool | None = typer.Option(None, "--https", help="Enable HTTPS"),
    certfile: str | None = typer.Option(None, "--certfile", help="Path to SSL cert"),
    keyfile: str | None = typer.Option(None, "--keyfile", help="Path to SSL key"),
    reload: bool | None = typer.Option(None, "--reload", help="Auto-reload on code changes"),
    workers: int | None = typer.Option(None, "--workers", help="Number of worker processes"),
):
    cfg = _resolve_server_config(host, port, https, certfile, keyfile, reload, workers)
    _start(**cfg)
