#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path

def run(cmd, shell=False):
    """Run a shell command with logging and error handling."""
    print(f"➡️  Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    result = subprocess.run(cmd, shell=shell)
    if result.returncode != 0:
        sys.exit(f"[ERROR] Command failed: {cmd}")

def uninstall_prefiq():
    """Uninstall existing prefiq and remove duplicate binaries."""
    print("🔍 Checking for existing prefiq installation...")

    # Step 1: Uninstall pip-installed prefiq in current Python environment
    result = subprocess.run([sys.executable, "-m", "pip", "show", "prefiq"], stdout=subprocess.DEVNULL)
    if result.returncode == 0:
        print("[WARN] prefiq is installed via pip. Uninstalling...")
        run([sys.executable, "-m", "pip", "uninstall", "-y", "prefiq"])
    else:
        print("[OK] No pip-installed prefiq found in current environment.")

    # Step 2: Remove system/global prefiq binaries (outside current venv)
    print("🧹 Checking system for duplicate prefiq executables...")

    try:
        which_cmd = "where" if os.name == "nt" else "which -a"
        result = subprocess.run(which_cmd.split() + ["prefiq"], capture_output=True, text=True)
        found_paths = result.stdout.strip().splitlines()

        removed = False
        for path in found_paths:
            path = path.strip()
            # Ignore paths inside current venv or sys.prefix (pyenv/virtualenv)
            if str(Path(sys.prefix)) in path:
                continue
            try:
                print(f"[WARN] Found duplicate prefiq at: {path}")
                os.remove(path)
                print(f"✅ Removed: {path}")
                removed = True
            except Exception as e:
                print(f"⚠️ Could not remove {path}: {e}")

        if not removed:
            print("[OK] No conflicting prefiq executables found outside the current environment.")
    except Exception as e:
        print(f"⚠️ Could not complete duplicate check: {e}")

def clean_build_artifacts():
    """Delete build/, dist/, and *.egg-info for a clean install."""
    print("🧹 Cleaning up build artifacts...")
    for folder in ["build", "dist"]:
        shutil.rmtree(folder, ignore_errors=True)
    for item in Path(".").glob("*.egg-info"):
        shutil.rmtree(item, ignore_errors=True)

def install_editable():
    """Install the local package in editable (-e) mode."""
    print("📦 Installing prefiq in editable mode...")
    run([sys.executable, "-m", "pip", "install", "-e", "."])

def find_cli_path():
    """Try to find the CLI path from multiple common locations."""
    candidates = []

    # Priority 1: local venvs
    if os.name == "nt":
        candidates.append(Path("venv/Scripts/prefiq.exe"))
        candidates.append(Path(".venv/Scripts/prefiq.exe"))
    else:
        candidates.append(Path("venv/bin/prefiq"))
        candidates.append(Path(".venv/bin/prefiq"))

    # Priority 2: pyenv or global via PATH
    try:
        result = subprocess.run(["which", "prefiq"], capture_output=True, text=True)
        cli_path = result.stdout.strip()
        if cli_path:
            candidates.append(Path(cli_path))
    except Exception:
        pass

    # Return the first existing CLI path
    for path in candidates:
        if path.exists():
            return path.resolve()

    return None

def verify_installation():
    """Check if the prefiq CLI is functional."""
    print("🚀 Verifying installation...")

    cli_path = find_cli_path()

    if not cli_path:
        print("❌ Could not find the 'prefiq' CLI in venv, .venv, or PATH.")
        print("💡 Try running manually:")
        print("   prefiq --help")
        sys.exit(1)

    try:
        result = subprocess.run([str(cli_path), "--help"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ prefiq CLI is working at: {cli_path}")
            print(result.stdout.splitlines()[0])
        else:
            raise RuntimeError("CLI returned non-zero exit code.")
    except Exception as e:
        print(f"❌ CLI verification failed: {e}")
        print(f"💡 Try running manually:\n   {cli_path} --help")
        sys.exit(1)

def rehash_pyenv_shim():
    """If using pyenv, rehash to generate shim for prefiq."""
    pyenv_root = os.getenv("PYENV_ROOT", str(Path.home() / ".pyenv"))
    pyenv_bin = Path(pyenv_root) / "bin" / "pyenv"
    if pyenv_bin.exists():
        print("🔁 Detected pyenv. Running rehash to regenerate shims...")
        try:
            run([str(pyenv_bin), "rehash"])
            shim_path = Path(pyenv_root) / "shims" / "prefiq"
            if shim_path.exists():
                print(f"✅ Global pyenv shim created at: {shim_path}")
            else:
                print("⚠️  Rehash ran but prefiq shim not found.")
        except Exception as e:
            print(f"⚠️  Failed to rehash pyenv: {e}")


def main():
    uninstall_prefiq()          # Remove any existing installations
    clean_build_artifacts()     # Remove build/ and egg-info
    install_editable()          # Install the latest version in editable mode
    rehash_pyenv_shim()
    verify_installation()       # Confirm CLI is working correctly

if __name__ == "__main__":
    main()
