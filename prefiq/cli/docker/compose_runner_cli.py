import typer
import json
from typing import Optional
from pathlib import Path
from prefiq.docker.utils.docker_manage_services import find_compose_files
from prefiq.docker.prepare.site_compose import create_site_compose
from prefiq.docker.prepare.mariadb_compose import create_mariadb_compose
from prefiq.docker.prepare.nginx_compose import create_nginx_compose

docker_run_cmd = typer.Typer()


@docker_run_cmd.command("up", help="Start Docker containers from compose files")
def up(
        dry_run: bool = typer.Option(False, "--dryrun", help="Preview actions without executing"),
        recreate: bool = typer.Option(False, "--recreate", help="Recreate compose files before running"),
        yes: bool = typer.Option(False, "--yes", "--no-input", help="Skip prompts and auto-confirm actions"),
        compose_dir: Optional[Path] = typer.Option(None, "--compose-dir", help="Directory to look for compose files"),
        output: Optional[str] = typer.Option(None, "--output", help="Output format (e.g., json)")
):
    typer.echo("👋 Hai from docker up")

    # Ask for compose_dir if not provided
    if recreate and not compose_dir:
        prompt_msg = typer.style("Enter directory to recreate and scan for docker-compose files",
                                 fg=typer.colors.YELLOW)
        user_input = typer.prompt(prompt_msg, default="docker")
        compose_dir = Path(user_input).expanduser().resolve()

    compose_dir = compose_dir or Path("docker")

    typer.echo(f"🔍 Searching compose files in: {compose_dir}")

    try:
        compose_files = find_compose_files(compose_dir)
    except Exception as e:
        typer.echo(typer.style(f"❌ {str(e)}", fg=typer.colors.RED))
        raise typer.Exit(1)

    if not compose_files:
        typer.echo(typer.style("⚠️ No Docker Compose files found.", fg=typer.colors.RED))

        if yes:
            choice = "a"
        else:

            choice = typer.prompt(typer.style("Recreate compose files? (a)ll / (s)elect / (n)o", fg=typer.colors.GREEN),
                                  default="a").lower()

        if choice == "a":
            domain = typer.prompt("🌐 Enter site domain", default="site.com")
            port = typer.prompt("🔢 Enter site port", default=8000)
            create_site_compose(domain, port, compose_dir)
            create_mariadb_compose(compose_dir)
            create_nginx_compose(compose_dir)
        elif choice == "s":
            if typer.confirm("Create site compose?", default=True):
                domain = typer.prompt("🌐 Enter site domain", default="site.com")
                port = typer.prompt("🔢 Enter site port", default=8000)
                create_site_compose(domain, port, compose_dir)

            if typer.confirm("Create database compose (MariaDB/Postgres)?", default=True):
                create_mariadb_compose(compose_dir)

            if typer.confirm("Create proxy compose (NGINX/Traefik)?", default=True):
                create_nginx_compose(compose_dir)
        else:
            typer.echo("❌ No compose files to start. Exiting.")
            raise typer.Exit()

        compose_files = find_compose_files(compose_dir)

    if output == "json":
        typer.echo(json.dumps({
            "compose_dir": str(compose_dir),
            "compose_files": [str(f) for f in compose_files],
            "dry_run": dry_run,
            "recreate": recreate
        }, indent=2))
    else:
        typer.echo(typer.style("[list]", fg=typer.colors.BRIGHT_CYAN) + " Compose files found:")

        for idx, file in enumerate(compose_files, start=1):
            file_str = str(file).lower()

            if "dockerfile" in file_str:
                color = typer.colors.MAGENTA
                label = "DOCKERFILE"
            elif "docker-compose-mariadb" in file_str or "docker-compose-postgres" in file_str:
                color = typer.colors.YELLOW
                label = "DATABASE"
            elif "docker-compose-nginx" in file_str or "docker-compose-traefik" in file_str:
                color = typer.colors.CYAN
                label = "PROXY"
            elif "docker-compose" in file_str or "site" in file_str:
                color = typer.colors.GREEN
                label = "SITE"
            else:
                color = typer.colors.WHITE
                label = "OTHER"

            label_styled = typer.style(f"[{label}]", fg=color, bold=True)
            typer.echo(f" -[{idx}] {label_styled} {file}")
