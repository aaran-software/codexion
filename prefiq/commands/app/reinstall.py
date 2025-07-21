import os

from prefiq.commands.app import install, uninstall
from prefiq.utils.path import get_apps_dir
from prefiq.utils.ui import print_success, print_warning


def run(args):

    app_path = os.path.join(get_apps_dir(), args.name)
    print_warning(f"Reinstalling app '{args.name}' at {app_path}...")

    uninstall.run(args)
    install.run(args)

    print_success(f"Reinstallation of '{args.name}' complete.")
