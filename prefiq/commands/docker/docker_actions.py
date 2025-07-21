import typer

from prefiq.commands.docker.dockerfile import generate_dockerfile

dockit_app = typer.Typer(help="Docker-related utilities")

@dockit_app.command("dockfile")
def create_dockfile(
    name: str = typer.Argument(..., help="Custom Dockerfile name (e.g., sundar)"),
    base: str = typer.Option("python:3.11", "--base", help="Base image"),
    workdir: str = typer.Option("/app", "--workdir", help="Working directory"),
    copy: list[str] = typer.Option([".:."], "--copy", help="COPY instructions (SRC:DST)"),
    run: list[str] = typer.Option([], "--run", help="RUN instructions"),
    cmd: str = typer.Option('"python", "main.py"', "--cmd", help="CMD to run")
):
    copy_instructions = []
    for item in copy:
        parts = item.split(":")
        if len(parts) != 2:
            raise typer.BadParameter("COPY format must be SRC:DST")
        copy_instructions.append((parts[0], parts[1]))

    generate_dockerfile(
        name=name,
        base_image=base,
        workdir=workdir,
        copy_instructions=copy_instructions,
        run_commands=run,
        cmd=cmd
    )
