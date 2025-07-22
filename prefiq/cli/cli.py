# prefiq/cli.py
import typer

from prefiq.cli.config.app import app_cli

app = typer.Typer()
app.add_typer(app_cli.app_cmd, name="app")




def main():
     app()