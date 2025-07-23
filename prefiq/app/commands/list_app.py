import json
import os

from prefiq.docker.compose import CPATH
from prefiq.utils.cprint import cprint_warning, console, styled_text


def run():
    if not os.path.exists(CPATH.CONFIG):
        cprint_warning("[warn] No apps installed.")
        return

    with open(CPATH.CONFIG) as f:
        config = json.load(f)

    apps = config.get("apps", [])

    if not apps:
        cprint_warning("No apps installed.")
        return

    for app in apps:
        console.cprint(styled_text(app), style="bold red")
