import typer
from prefiq.docker.compose.manage import docker_up

docker_run_cmd = typer.Typer()

@docker_run_cmd.command("up")
def up():
    docker_up()
