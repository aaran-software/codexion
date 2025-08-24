# prefiq/apps/app_stubs.py
from __future__ import annotations
from datetime import datetime

def ts() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def stub_readme(app_name: str) -> str:
    return f"""# {app_name}

This app was scaffolded by Prefiq.

## Structure

- bin/
- core/
- database/migrations/
- database/seeders/
- public/
- src/
- providers/
- docs/
- assets/
"""

def stub_gitkeep() -> str:
    return ""  # empty file, just to keep folders in VCS

def stub_init_py(app_name: str) -> str:
    return f"""# {app_name} package
__all__ = ["core", "src", "providers", "database", "bin", "public", "docs", "assets"]
"""

def stub_provider(app_name: str) -> str:
    class_name = f"{app_name.capitalize()}Provider"
    return f'''# providers/{class_name}.py
# Auto-registered Provider for {app_name}
from prefiq.core.provider import Provider  # your base Provider

class {class_name}(Provider):
    abstract = False
    enabled  = True
    name     = "{app_name}"
    order    = None  # will be injected/overridden by config during boot if needed

    def register(self) -> None:
        # bind services, singletons, configs
        pass

    def boot(self) -> None:
        # run boot-time hooks after all providers are registered
        pass
'''

def stub_migration(app_name: str) -> str:
    file_ts = ts()
    return f'''# database/migrations/{file_ts}_init.py
from prefiq.database.migrations.base import Migrations

class Init(Migrations):
    APP_NAME    = "{app_name}"
    TABLE_NAME  = "{app_name}_example"
    ORDER_INDEX = 0

    def up(self) -> None:
        self.create(self.TABLE_NAME, lambda t: [
            t.id(),
            t.string("name"),
            t.timestamps(),
        ])

    def down(self) -> None:
        self.drop_if_exists(self.TABLE_NAME)
'''

def stub_pyproject(app_name: str) -> str:
    return f"""# Optional: customize if each app is a sub-package
# This is just a placeholder; safe to delete if not needed.
[tool.prefiq.app]
name = "{app_name}"
"""

def stub_cli_init(app_name: str) -> str:
    return f'''# src/cli/__init__.py
# Optional Typer commands for {app_name}
# import typer
# app = typer.Typer(help="{app_name} commands")
# @app.command()
# def hello(): print("Hello from {app_name}")
# __all__ = ["app"]
'''
