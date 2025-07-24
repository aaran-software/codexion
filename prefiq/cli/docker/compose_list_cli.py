from pathlib import Path
import typer

DOCKER_DIR = Path("docker")

def list_docker_assets(folder: Path = DOCKER_DIR):
    typer.echo("")
    typer.echo(f"📂 Scanning folder: {folder.resolve()}\n")

    dockerfiles = list(folder.glob("Dockerfile*"))
    compose_files = list(folder.glob("docker-compose-*.yml"))

    # Grouping
    site_composes = [f for f in compose_files if "mariadb" not in f.name and "postgres" not in f.name and "nginx" not in f.name and "traefik" not in f.name]
    db_composes = [f for f in compose_files if "mariadb" in f.name or "postgres" in f.name]
    proxy_composes = [f for f in compose_files if "nginx" in f.name or "traefik" in f.name]

    # Dockerfiles
    typer.echo("🐳 Dockerfiles:")
    for file in dockerfiles:
        typer.echo(f"  ✔ {file.name}")
    typer.echo("")

    # Site Compose Files
    typer.echo("📦 Docker Compose (Site files):")
    for file in site_composes:
        typer.echo(f"  ✔  {file.name}")
    typer.echo("")

    # DB Compose Files
    typer.echo("🛢️ Database Compose Files:")
    for file in db_composes:
        db_type = "MariaDB" if "mariadb" in file.name else "PostgreSQL"
        typer.echo(f"  ✔  {file.name:30} ({db_type})")
    typer.echo("")

    # Proxy Compose Files
    typer.echo("🌐 Reverse Proxy Compose Files:")
    for file in proxy_composes:
        proxy_type = "Nginx" if "nginx" in file.name else "Traefik"
        typer.echo(f"  ✔ {file.name:30} ({proxy_type})")
    typer.echo("")

    typer.secho("✅ Scan complete.", fg=typer.colors.GREEN)