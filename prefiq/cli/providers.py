# prefiq/cli/providers.py
from __future__ import annotations
import typer
from prefiq.core.discovery import discover_providers

providers_app = typer.Typer(help="Discover and inspect Prefiq providers")

@providers_app.command("list")
def cmd_list() -> None:
    infos = discover_providers()
    if not infos:
        typer.echo("No providers discovered.")
        return

    typer.echo("Discovered providers:")
    for p in infos:
        ord_txt = f"{p.order}" if p.order is not None else "-"
        ver_txt = p.version or "-"
        typer.echo(f" • {p.app}  ({p.class_name})  v{ver_txt}  order={ord_txt}  [{p.module}]")

cli = providers_app
