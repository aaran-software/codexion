import typer
from prefiq.commands.utils.ui import print_success


def run(
    app: str = typer.Argument(..., help="App name")
):
    print_success(f"[OK] Pushed changes for {app} (mocked)")
