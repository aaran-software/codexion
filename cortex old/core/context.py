# cortex/core/context.py

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from cortex.core.settings import get_settings
from pathlib import Path
from datetime import datetime
from cortex.core.vite import get_vite_assets


def mount_vite(app: FastAPI):
    """Mount the Vite static build directory at /build"""
    settings = get_settings()
    vite_build_path = Path(settings.project_root) / "public" / "backend" / "build"
    app.mount("/build", StaticFiles(directory=vite_build_path), name="vite-build")


def template_context(request: Request):
    """Inject common template variables into all Jinja2 templates"""
    settings = get_settings()
    return {
        "request": request,
        "settings": settings,
        "year": datetime.now().year,
        "app_name": "Codexion" if not hasattr(settings, "APP_NAME") else getattr(settings, "APP_NAME"),
        "vite": {
            "vite_asset": get_vite_assets
        }
    }
