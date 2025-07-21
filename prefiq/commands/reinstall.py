import os

from prefiq.commands import uninstall, install
from prefiq.utils.path import get_apps_dir


def run(args):

    app_path = os.path.join(get_apps_dir(), args.name)
    print(f"[REINSTALL] Reinstalling app '{args.name}' at {app_path}...")

    uninstall.run(args)
    install.run(args)

    print(f"[ok] Reinstallation of '{args.name}' complete.", flush=True)
