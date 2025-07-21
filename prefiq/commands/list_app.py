# prefiq/commands/list.py

import json
import os

def run(args):
    config_path = os.path.join("apps", "config.json")
    if not os.path.exists(config_path):
        print("[warn] No apps installed.", flush=True)
        return

    with open(config_path) as f:
        config = json.load(f)

    apps = config.get("apps", [])
    for app in apps:
        print(app, flush=True)
