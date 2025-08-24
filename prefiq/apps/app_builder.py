# prefiq/apps/app_builder.py

from __future__ import annotations

import shutil
from pathlib import Path

from prefiq.apps.app_scaffold import (
    APP_ROOT,
    DEFAULT_VERSION,
    AppError,
    assert_valid_name,
    write_scaffold,
    cfg_lists_app_but_folder_missing,
)
from prefiq.apps.app_cfg import load_cfg, save_cfg, has_app, remove_app


def new_app(name: str, *, version: str = DEFAULT_VERSION) -> Path:
    """
    Create a brand-new app at apps/<name>.
    - If folder exists -> error (no destructive action).
    - If cfg has app but folder missing -> allowed; will recreate folder tree.
    """
    assert_valid_name(name)
    base = APP_ROOT / name

    # if directory already exists, do not proceed
    if base.exists():
        raise AppError(f"App folder already exists at {base}")

    # it's okay if cfg lists the app and folder's missing — we just scaffold it now
    # caller can choose to surface a warning if desired:
    _cfg_mismatch = cfg_lists_app_but_folder_missing(name)

    return write_scaffold(name, version=version)


def drop_app(name: str, force: bool = False) -> None:
    """
    Remove app folder and unregister from apps.cfg.
    - If folder missing: still unregister from cfg.
    - If folder exists and not force: raise.
    """
    assert_valid_name(name)
    base = APP_ROOT / name

    if base.exists():
        if not force:
            raise AppError(f"Refusing to drop '{name}' without --force (folder {base} exists).")
        shutil.rmtree(base)

    # unregister from cfg if present
    cp = load_cfg()
    if has_app(cp, name):
        remove_app(cp, name)
        save_cfg(cp)


def reinstall_app(name: str, force: bool = False, *, version: str = DEFAULT_VERSION) -> Path:
    """
    Drop then recreate a fresh scaffold for apps/<name>.
    Version is written to apps.cfg (version-only format).
    """
    assert_valid_name(name)

    # Always force drop here (ignore errors if already gone)
    try:
        drop_app(name, force=True)
    except AppError:
        # ignore
        pass

    # Recreate via shared scaffold
    return write_scaffold(name, version=version)
