import subprocess
import json
import typer
import yaml
from pathlib import Path
from typing import List, Optional, Dict, Any

from prefiq import CPATH
from prefiq.docker.utils.docker_checks import (
    is_docker_running,
    get_docker_version,
    get_running_containers,
)

DEFAULT_FOLDER = CPATH.DOCKER_DIR


class DockerComposeManager:
    report: Dict[str, Any]

    def __init__(
        self,
        folder: Path = DEFAULT_FOLDER,
        sites: Optional[List[str]] = None,
        recreate: bool = False,
        dry_run: bool = False,
        json_output: bool = False,
    ):
        self.folder = folder
        self.sites = sites
        self.recreate = recreate
        self.dry_run = dry_run
        self.json_output = json_output
        self.report = {
            "docker_running": False,
            "docker_version": None,
            "selected_sites": sites,
            "folder": str(folder),
            "planned_services": [],
            "status": [],
        }

    def run(self):
        if not self.check_docker():
            return
        self.report["docker_version"] = get_docker_version()
        if self.recreate:
            self.recreate_compose_files()
        site_files = self.get_site_compose_files()
        self.report["planned_services"] = [f.name for f in site_files]
        self.report["running_containers"] = get_running_containers()
        if self.dry_run:
            self.display_dry_run(site_files)
            return
        self.run_compose_files(site_files)
        if self.json_output:
            self.display_json_report()

    def check_docker(self) -> bool:
        self.report["docker_running"] = is_docker_running()
        if not self.report["docker_running"]:
            typer.secho("❌ Docker is not running!", fg=typer.colors.RED)
            if self.json_output:
                self.display_json_report()
            raise typer.Exit(1)
        return True

    def recreate_compose_files(self):
        typer.secho("♻️ Recreating docker-compose files...", fg=typer.colors.YELLOW)
        # TODO: Hook to regenerate compose files based on self.sites
        pass

    def get_site_compose_files(self) -> List[Path]:
        all_files = list(self.folder.glob("docker-compose-*.yml"))
        site_files = [
            f for f in all_files
            if not any(x in f.name for x in ["mariadb", "postgres", "nginx", "traefik"])
        ]
        if self.sites:
            site_files = [f for f in site_files if any(s in f.name for s in self.sites)]
        return site_files

    def display_dry_run(self, site_files: List[Path]):
        typer.secho("🧪 Dry run mode enabled. The following would be started:", fg=typer.colors.BLUE)
        for f in site_files:
            typer.echo(f"  - {f.name}")
        if self.json_output:
            self.display_json_report()

    def run_compose_files(self, site_files: List[Path]):
        for file in site_files:
            compose_file = self.folder / file.name
            if not compose_file.exists():
                typer.secho(f"⚠️ File not found: {compose_file}", fg=typer.colors.RED)
                self.report["status"].append({
                    "file": file.name,
                    "status": "missing"
                })
                continue

            # Optionally validate Dockerfile existence
            if not self.has_valid_dockerfile(compose_file):
                continue

            typer.secho(f"🔧 Running: docker compose -f {file.name} up -d", fg=typer.colors.CYAN)
            result = subprocess.run(
                ["docker", "compose", "-f", compose_file.name, "up", "-d"],
                cwd=self.folder
            )
            status = "success" if result.returncode == 0 else "failed"
            self.report["status"].append({"file": file.name, "status": status})
            if status == "failed":
                typer.secho(f"❌ Failed to start: {file.name}", fg=typer.colors.RED)

    def has_valid_dockerfile(self, compose_path: Path) -> bool:
        """Check if all build services in the compose file have a Dockerfile."""
        try:
            with open(compose_path, "r") as f:
                content = yaml.safe_load(f)
                services = content.get("services", {})
                for name, service in services.items():
                    if "build" in service:
                        build = service["build"]
                        if isinstance(build, str):
                            build_path = Path(build)
                        elif isinstance(build, dict):
                            context = build.get("context", ".")
                            build_path = Path(context)
                        else:
                            self.report["status"].append({
                                "file": compose_path.name,
                                "status": f"❌ Invalid 'build' format for service '{name}'"
                            })
                            return False

                        dockerfile = build_path / "Dockerfile"
                        if not dockerfile.exists():
                            self.report["status"].append({
                                "file": compose_path.name,
                                "status": f"❌ Missing Dockerfile at {dockerfile}"
                            })
                            return False
            return True
        except Exception as e:
            self.report["status"].append({
                "file": compose_path.name,
                "status": f"❌ Failed to parse YAML: {e}"
            })
            return False

    def display_json_report(self):
        print(json.dumps(self.report, indent=2))
