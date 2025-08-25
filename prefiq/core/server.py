# prefiq/cli/core/server.py

from __future__ import annotations
import typer
import uvicorn
from prefiq.core.application import Application

server_app = typer.Typer(help="Run HTTP/HTTPS server")

@server_app.command("start")
def start(
    host: str = "0.0.0.0",
    port: int = 5001,
    https: bool = typer.Option(False, "--https", help="Enable HTTPS"),
    certfile: str = typer.Option(None, "--certfile", help="Path to SSL cert"),
    keyfile: str = typer.Option(None, "--keyfile", help="Path to SSL key"),
):
    app = Application.get_app().resolve("http.app")
    if app is None:
        typer.echo("❌ No HTTP app bound. Did you register HttpProvider?")
        raise typer.Exit(code=1)

    if https and (not certfile or not keyfile):
        typer.echo("❌ --certfile and --keyfile required for HTTPS")
        raise typer.Exit(code=1)

    uvicorn.run(
        app,
        host=host,
        port=port,
        ssl_certfile=certfile if https else None,
        ssl_keyfile=keyfile if https else None,
    )
