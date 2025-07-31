import json
from pathlib import Path
from cortex.core.settings import get_settings

settings = get_settings()

# Construct manifest path using project_root
manifest_path = Path(settings.project_root) / "public" / "backend" / "build" / ".vite" / "manifest.json"

# Load manifest safely
vite_manifest = {}
if manifest_path.exists():
    try:
        with manifest_path.open("r", encoding="utf-8") as f:
            vite_manifest = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error loading Vite manifest: {e}")


def get_vite_assets(entry: str):
    asset = vite_manifest.get(entry)
    if not asset:
        return {"js_file": None, "css_files": []}

    return {
        "js_file": f"/build/{asset.get('file')}" if asset.get("file") else None,
        "css_files": [f"/build/{css}" for css in asset.get("css", [])],
    }
