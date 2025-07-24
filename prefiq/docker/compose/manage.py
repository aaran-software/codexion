import typer

def docker_run_cmd(dry_run: bool = False, recreate: bool = False, json_output: bool = False):
    typer.secho("👋 Hai from docker up", fg=typer.colors.GREEN)
    typer.echo(f"dry_run: {dry_run}")
    typer.echo(f"recreate: {recreate}")
    typer.echo(f"json_output: {json_output}")

