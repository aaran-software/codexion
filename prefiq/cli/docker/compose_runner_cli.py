import typer
import json
from typing import Optional
from pathlib import Path

from prefiq.docker.prepare.postgres_compose import create_postgres_compose
from prefiq.docker.utils.docker_manage_services import find_compose_files
from prefiq.docker.prepare.site_compose import create_site_compose
from prefiq.docker.prepare.mariadb_compose import create_mariadb_compose
from prefiq.docker.prepare.nginx_compose import create_nginx_compose
from prefiq.docker.prepare.traefik_compose import create_traefik_compose

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

    if recreate and not compose_dir:
        prompt_msg = typer.style("Enter directory to recreate and scan for docker-compose files", fg=typer.colors.YELLOW)
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
            choice = typer.prompt(
                typer.style("Recreate compose files? (a)ll / (s)elect / (n)o", fg=typer.colors.GREEN),
                default="a"
            ).lower()

        if choice == "a":
            # --- Site ---
            domain = typer.prompt("🌐 Enter site domain", default="site.com")
            port = typer.prompt("🔢 Enter site port", default=8000)
            create_site_compose(domain, port, compose_dir)

            # --- Database ---
            db = typer.prompt("Which database to use? (mariadb / postgres)", default="mariadb").lower()

            if db == "mariadb":
                mariadb_name = typer.prompt("🛢️  MariaDB - DB name", default=domain)
                mariadb_password = typer.prompt("🔑 MariaDB - Password", default="password123")
                create_mariadb_compose(name=mariadb_name, password=mariadb_password, output_dir=compose_dir)
            else:
                pg_name = typer.prompt("🛢️  Postgres - DB name", default=domain)
                pg_password = typer.prompt("🔑 Postgres - Password", default="password123")
                create_postgres_compose(name=pg_name, password=pg_password, output_dir=compose_dir)

            # --- Proxy ---
            proxy = typer.prompt("Which proxy to use? (traefik / nginx)", default="traefik").lower()
            if proxy == "nginx":
                create_nginx_compose(service_name=domain, service_port=port, output_dir=compose_dir)
            else:
                email = typer.prompt("📧 Admin email (for Let's Encrypt)", default="admin@example.com")
                dash_domain = typer.prompt("🌐 Traefik dashboard domain", default=f"traefik.{domain}")
                admin_user = typer.prompt("👤 Dashboard user", default="admin")
                admin_pass = typer.prompt("🔐 Dashboard password", default="admin123")
                create_traefik_compose(
                    email=email,
                    dashboard_domain=dash_domain,
                    admin_user=admin_user,
                    admin_password=admin_pass,
                    output_dir=compose_dir
                )

        elif choice == "s":
            if typer.confirm("Create site compose?", default=True):
                domain = typer.prompt("🌐 Enter site domain", default="site.com")
                port = typer.prompt("🔢 Enter site port", default=8000)
                create_site_compose(domain, port, compose_dir)

            if typer.confirm("Create MariaDB compose?", default=True):
                mariadb_name = typer.prompt("MariaDB name", default="site.com")
                mariadb_password = typer.prompt("MariaDB password", default="secret")
                create_mariadb_compose(name=mariadb_name, password=mariadb_password, output_dir=compose_dir)

            if typer.confirm("Create NGINX compose?", default=True):
                create_nginx_compose(service_name=domain, service_port=port, output_dir=compose_dir)

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
                label, color = "DOCKERFILE", typer.colors.MAGENTA
            elif "mariadb" in file_str or "postgres" in file_str:
                label, color = "DATABASE", typer.colors.YELLOW
            elif "nginx" in file_str or "traefik" in file_str:
                label, color = "PROXY", typer.colors.CYAN
            elif "compose" in file_str:
                label, color = "SITE", typer.colors.GREEN
            else:
                label, color = "OTHER", typer.colors.WHITE

            typer.echo(f" -[{idx}] {typer.style(f'[{label}]', fg=color, bold=True)} {file}")
