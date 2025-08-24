# prefiq/apps/app_scaffold.py

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict

from prefiq.apps.app_stubs import (
    stub_readme, stub_gitkeep, stub_init_py, stub_provider,
    stub_migration, stub_pyproject, stub_cli_init, ts,
)
from prefiq.apps.app_cfg import load_cfg, save_cfg, add_app, has_app

APP_ROOT = Path("apps")
DEFAULT_VERSION = "0.1.0"
_VALID = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")


class AppError(RuntimeError):
    pass


def assert_valid_name(name: str) -> None:
    if not name or not _VALID.match(name):
        raise AppError(
            f"Invalid app name '{name}'. Use letters, numbers, underscores; cannot start with a digit."
        )


def structure(base: Path) -> Dict[str, Path]:
    """Return the canonical app folders."""
    return {
        "bin": base / "bin",
        "core": base / "core",
        "migrations": base / "database" / "migrations",
        "seeders": base / "database" / "seeders",
        "public": base / "public",
        "src": base / "src",
        "providers": base / "providers",
        "docs": base / "docs",
        "assets": base / "assets",
    }


def _mk(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def _write(path: Path, content: str, *, overwrite: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        return
    path.write_text(content, encoding="utf-8")


def _touch_gitkeep(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(stub_gitkeep(), encoding="utf-8")


def write_provider_stub(app_name: str, providers_dir: Path) -> Path:
    cls_file = providers_dir / f"{app_name.capitalize()}Provider.py"
    _write(cls_file, stub_provider(app_name))
    # providers package init
    _write(providers_dir / "__init__.py", f"# providers package for {app_name}\n", overwrite=False)
    return cls_file


def write_scaffold(name: str, *, version: str = DEFAULT_VERSION) -> Path:
    """
    Idempotently create the app directory tree and write all basic stubs.
    Assumes the target base folder does NOT exist (caller enforces).
    Also ensures the app is present in apps.cfg with its version.
    """
    assert_valid_name(name)
    base = APP_ROOT / name
    paths = structure(base)

    # folders
    for p in paths.values():
        _mk(p)

    # package init
    _write(base / "__init__.py", stub_init_py(name))

    # provider
    write_provider_stub(name, paths["providers"])

    # first migration
    mig_file = paths["migrations"] / f"{ts()}_init.py"
    _write(mig_file, stub_migration(name))

    # optional files
    _write(base / "README.md", stub_readme(name), overwrite=False)
    _write(base / "pyproject.toml", stub_pyproject(name), overwrite=False)
    _write(paths["src"] / "cli" / "__init__.py", stub_cli_init(name), overwrite=False)

    # gitkeep empties
    for key in ("seeders", "public", "docs", "assets", "bin", "core"):
        _touch_gitkeep(paths[key] / ".gitkeep")

    # config (version‑only, file order drives boot order)
    cp = load_cfg()
    add_app(cp, name, version=version)
    save_cfg(cp)

    return base


def cfg_lists_app_but_folder_missing(name: str) -> bool:
    """
    True if apps.cfg has the app but the folder does not exist.
    """
    cp = load_cfg()
    return has_app(cp, name) and not (APP_ROOT / name).exists()
