import typer
import json
from typing import Optional
from pathlib import Path

from prefiq.docker.compose.manage import show_services_preview, run_docker_up
from prefiq.docker.prepare.dockerfile_default import create_docker
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

    # Ask for compose_dir if not provided
    if recreate and not compose_dir:
        prompt_msg = typer.style("Enter directory to recreate and scan for docker-compose files",
                                 fg=typer.colors.YELLOW)
        user_input = typer.prompt(prompt_msg, default="docker")
        compose_dir = Path(user_input).expanduser().resolve()

    compose_dir = compose_dir or Path("docker")

    if not compose_dir.exists():
        typer.echo(typer.style(f"📁 Creating directory: {compose_dir}", fg=typer.colors.BLUE))
        compose_dir.mkdir(parents=True, exist_ok=True)

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
            # SITE
            domain = typer.prompt("🌐 Enter site domain", default="site.com")
            port = typer.prompt("🔢 Enter site port", default=8000)

            create_docker(compose_dir)

            create_site_compose(domain, port, compose_dir)

            # DATABASE
            db = typer.prompt("💾 Select database (mariadb / postgres)?", default="mariadb")
            if db == "mariadb":

                mariadb_name = typer.prompt("🔐 MariaDB username", default="root")
                mariadb_password = typer.prompt("🔐 Enter MariaDB password", default="secret", hide_input=True)
                create_mariadb_compose(name=mariadb_name, password=mariadb_password, output_dir=compose_dir)
            else:

                pg_name = typer.prompt("🔐 Postgres username", default="root")
                pg_password = typer.prompt("🔐 Enter Postgres password", default="secret", hide_input=True)
                create_postgres_compose(name=pg_name, password=pg_password, output_dir=compose_dir)

            # REVERSE PROXY
            proxy = typer.prompt("🌐 Select reverse proxy (traefik / nginx)?", default="traefik")

            if proxy == "traefik":
                email = typer.prompt("📧 Enter admin email", default="admin@site.com")
                dash_domain = typer.prompt("🌐 Dashboard domain (optional)", default="dashboard.site.com")
                traefik_user = typer.prompt("👤 Admin user (optional)", default="admin")
                traefik_pass = typer.prompt("🔐 Admin password (optional)", default="adminpass")
                create_traefik_compose(
                    email=email,
                    dashboard_domain=dash_domain,
                    admin_user=traefik_user,
                    admin_password=traefik_pass,
                    output_dir=compose_dir
                )
            else:
                service_name = typer.prompt("🌍 Enter service name for NGINX", default=domain)
                service_port = typer.prompt("🔢 Enter service port for NGINX", default=port)
                create_nginx_compose(service_name, int(service_port), output_dir=compose_dir)

        elif choice == "s":
            # Selective compose creation
            if typer.confirm("Create site compose?", default=True):
                domain = typer.prompt("🌐 Enter site domain", default="site.com")
                port = typer.prompt("🔢 Enter site port", default=8000)
                create_site_compose(domain, port, compose_dir)

            if typer.confirm("Create database compose?", default=True):
                db = typer.prompt("💾 Select database (mariadb / postgres)?", default="mariadb")
                if db == "mariadb":
                    name = typer.prompt("🔐 MariaDB username", default="root")
                    pwd = typer.prompt("🔐 Enter MariaDB password", default="secret", hide_input=True)
                    create_mariadb_compose(name=name, password=pwd, output_dir=compose_dir)
                else:
                    name = typer.prompt("🔐 Postgres username", default="root")
                    pwd = typer.prompt("🔐 Enter Postgres password", default="secret", hide_input=True)
                    create_postgres_compose(name=name, password=pwd, output_dir=compose_dir)

            if typer.confirm("Create reverse proxy compose?", default=True):
                proxy = typer.prompt("🌐 Select reverse proxy (traefik / nginx)?", default="traefik")
                if proxy == "traefik":
                    email = typer.prompt("📧 Enter admin email", default="admin@site.com")
                    dash_domain = typer.prompt("🌐 Dashboard domain (optional)", default="dashboard.site.com")
                    traefik_user = typer.prompt("👤 Admin user (optional)", default="admin")
                    traefik_pass = typer.prompt("🔐 Admin password (optional)", default="adminpass")
                    create_traefik_compose(
                        email=email,
                        dashboard_domain=dash_domain,
                        admin_user=traefik_user,
                        admin_password=traefik_pass,
                        output_dir=compose_dir
                    )
                else:
                    service_name = typer.prompt("🌍 Enter service name for NGINX", default="site.com")
                    service_port = typer.prompt("🔢 Enter service port for NGINX", default=8000)
                    create_nginx_compose(service_name, int(service_port), output_dir=compose_dir)

        else:
            typer.echo("❌ No compose files to start. Exiting.")
            raise typer.Exit()

        compose_files = find_compose_files(compose_dir)

    # Final Output
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
                color, label = typer.colors.MAGENTA, "DOCKERFILE"
            elif "mariadb" in file_str or "postgres" in file_str:
                color, label = typer.colors.YELLOW, "DATABASE"
            elif "nginx" in file_str or "traefik" in file_str:
                color, label = typer.colors.CYAN, "PROXY"
            elif "compose" in file_str:
                color, label = typer.colors.GREEN, "SITE"
            else:
                color, label = typer.colors.WHITE, "OTHER"
            typer.echo(f" -[{idx}] {typer.style(f'[{label}]', fg=color, bold=True)} {file}")

    # show services preview
    all_services = show_services_preview(compose_files)

    # confirm
    if typer.confirm("\nDo you want to start these containers?", default=True):
        run_docker_up(compose_files)
        typer.echo(typer.style("\n✅ Docker containers started.", fg=typer.colors.GREEN))
    else:
        typer.echo(typer.style("\n⏹️ Cancelled. No containers started.", fg=typer.colors.YELLOW))
