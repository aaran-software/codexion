# cortex/core/startup.py

import os
import secrets
import shutil

ENV_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ENV_PATH = os.path.join(ENV_DIR, ".env")
ENV_SAMPLE_PATH = os.path.join(ENV_DIR, ".env.sample")

def ensure_env_file():
    """Run once before settings load. Creates .env if missing."""
    if not os.path.exists(ENV_PATH):
        print("[STARTUP] .env not found. Creating from .env.sample...")
        shutil.copyfile(ENV_SAMPLE_PATH, ENV_PATH)
        secret = secrets.token_urlsafe(32)
        with open(ENV_PATH, "a") as f:
            f.write(f"\nJWT_SECRET_KEY={secret}\n")
        print(f"[STARTUP] .env created and secret key added: {secret[:8]}...")
