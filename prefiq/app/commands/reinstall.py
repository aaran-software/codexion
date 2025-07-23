import os

from prefiq import CPATH
from prefiq.app.commands import uninstall, install
from prefiq.utils.cprint import cprint_success, cprint_warning


def run(name: str, force: bool = False):

    app_path = CPATH.APPS_DIR + name

    cprint_warning(f"Reinstalling app '{name}' at {app_path}...")

    uninstall.run(name=name)
    install.run(name=name, force=force)

    cprint_success(f"Reinstallation of '{name}' complete.")
