import typer
from prefiq.commands.utils.ui import print_success


def run(
    app: str = typer.Argument(..., help="App name")
):
    print_success("[OK] SSH key created and stored (mocked)")
