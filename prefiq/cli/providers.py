# prefiq/cli/providers.py
from __future__ import annotations
import typer
from prefiq.core.service_providers import get_service_providers  # ← use two-system loader

providers_app = typer.Typer(help="Discover and inspect Prefiq providers")

@providers_app.command("list")
def cmd_list() -> None:
    classes = get_service_providers()
    if not classes:
        typer.echo("No providers discovered.")
        return

    typer.echo("Discovered providers:")
    for cls in classes:
        name   = getattr(cls, "name", cls.__name__)
        order  = getattr(cls, "order", None)
        module = cls.__module__
        typer.echo(f" • {name}  ({cls.__name__})  order={order if order is not None else '-'}  [{module}]")
