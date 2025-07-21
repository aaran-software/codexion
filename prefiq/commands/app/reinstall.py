import os

from prefiq.commands.app import install, uninstall
from prefiq.utils.path import get_apps_dir
from prefiq.utils.ui import print_success, print_warning


def run(name: str, force: bool = False):
    app_path = os.path.join(get_apps_dir(), name)
    print_warning(f"Reinstalling app '{name}' at {app_path}...")

    uninstall.run(name=name)
    install.run(name=name, force=force)

    print_success(f"Reinstallation of '{name}' complete.")
