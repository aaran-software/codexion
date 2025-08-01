# prefiq/context.py

import os
from pathlib import Path
import sys


def get_codexion_root(check_exists=True) -> Path:
    """
    Returns the path to the codexion root directory.

    Priority:
    1. Environment variable CODEXION_HOME
    2. Default to ~/codexion

    Raises:
        SystemExit if check_exists=True and path doesn't exist.
    """
    env_path = os.environ.get("CODEXION_HOME")
    if env_path:
        codexion_path = Path(env_path).expanduser().resolve()
        print(f"[🔍] CODEXION_HOME set via env: {codexion_path}")
    else:
        codexion_path = Path.home() / "codexion"
        print(f"[ℹ️] CODEXION_HOME not set, defaulting to: {codexion_path}")

    if check_exists and not codexion_path.exists():
        print(f"[❌] Codexion path does not exist: {codexion_path}")
        print("💡 Set CODEXION_HOME or create the directory manually.")
        sys.exit(1)

    return codexion_path
