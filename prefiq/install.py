#!/usr/bin/env python3

import os
import subprocess
import sys
import shutil
import os
from pathlib import Path
import platform
from pathlib import Path

def run(cmd, shell=False):
    print(f"➡️  Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    result = subprocess.run(cmd, shell=shell)
    if result.returncode != 0:
        sys.exit(f"[ERROR] Command failed: {cmd}")

def uninstall_prefiq():
    print("🔍 Checking for existing prefiq installation...")
    result = subprocess.run(["pip", "show", "prefiq"], stdout=subprocess.DEVNULL)
    if result.returncode == 0:
        print("[WARN]  prefiq is already installed. Uninstalling...")
        run(["pip", "uninstall", "-y", "prefiq"])
    else:
        print("[OK] prefiq is not currently installed.")

def clean_build_artifacts():
    print("🧹 Cleaning up build artifacts...")
    for folder in ["build", "dist"]:
        shutil.rmtree(folder, ignore_errors=True)
    for item in Path(".").glob("*.egg-info"):
        shutil.rmtree(item, ignore_errors=True)

def install_editable():
    print("📦 Installing prefiq in editable mode...")
    run(["pip", "install", "-e", "."])

def add_venv_scripts_to_path():
    venv_scripts = Path(".venv") / ("Scripts" if os.name == "nt" else "bin")
    if venv_scripts.exists():
        os.environ["PATH"] = str(venv_scripts) + os.pathsep + os.environ.get("PATH", "")
        return str(venv_scripts)
    return None

def get_os_specific_hint():
    os_type = platform.system().lower()
    if os_type == "windows":
        return {
            "activate": ".venv\\Scripts\\activate.bat",
            "cli_path": ".venv\\Scripts\\prefiq.exe"
        }
    else:
        return {
            "activate": "source .venv/bin/activate",
            "cli_path": "./.venv/bin/prefiq"
        }

def verify_installation():
    print("🚀 Verifying installation...")
    try:
        result = subprocess.run(["prefiq", "--help"], capture_output=True, text=True)
        if result.returncode == 0:
            print("[OK] prefiq CLI installed successfully!")
            print(result.stdout.splitlines()[0])
            return
        else:
            raise RuntimeError("CLI failed to respond.")
    except Exception:
        print("[ERROR] Installation failed: 'prefiq' command not found.")

        hint = get_os_specific_hint()
        cli_path = Path(hint["cli_path"])
        if cli_path.exists():
            print(f"💡 Try running manually:\n   {hint['cli_path']}")
        print(f"💡 Or activate your virtual environment first:\n   {hint['activate']}")
        sys.exit(1)


def main():
    uninstall_prefiq()
    clean_build_artifacts()
    install_editable()
    add_venv_scripts_to_path()
    verify_installation()

if __name__ == "__main__":
    main()
