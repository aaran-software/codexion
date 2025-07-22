import typer
from prefiq.config.generate import generate_all_configs

config_cli = typer.Typer(help="Manage configuration files")

@config_cli.command("init", help="Generate default config files if missing")
def init_configs():
    generate_all_configs()
