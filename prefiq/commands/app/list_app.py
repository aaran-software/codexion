import json
import os
from prefiq.utils.path import get_config_path
from prefiq.utils.ui import styled_text, print_success, print_warning, console


def run():
    config_path = get_config_path()

    if not os.path.exists(config_path):
        print_warning("[warn] No apps installed.")
        return

    with open(config_path) as f:
        config = json.load(f)

    apps = config.get("apps", [])

    if not apps:
        print_warning("No apps installed.")
        return

    for app in apps:
        console.print(styled_text(app), style="bold red")
