import os
import sys
import subprocess
from pathlib import Path
import platform

REPO_URL = "https://github.com/AARAN-SOFTWARE/codexion.git"
PROJECT_DIR = Path("/home/devops/cloud/codexion")
MODE = os.environ.get("MODE", "dev")  # "prod" or "dev"


def run_command(cmd, check=True, shell=True):
    """Run a shell command."""
    print(f"[~] Running: {cmd}")
    subprocess.run(cmd, shell=shell, check=check)


def check_and_install_package(package_name, check_cmd, install_cmd):
    try:
        subprocess.run(check_cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"[✔] {package_name} already installed.")
    except subprocess.CalledProcessError:
        print(f"[!] {package_name} not found. Installing...")
        run_command(install_cmd)


def install_prefiq_editable():
    print("📦 Installing prefiq in editable mode...")
    run_command("pip install -e .")


def get_os_specific_hint():
    if platform.system() == "Windows":
        return {
            "activate": ".\\.venv\\Scripts\\activate",
            "cli_path": ".\\.venv\\Scripts\\prefiq.exe",
        }
    else:
        return {
            "activate": "source .venv/bin/activate",
            "cli_path": "./.venv/bin/prefiq",
        }


def verify_prefiq_installation():
    print("🚀 Verifying installation...")
    try:
        result = subprocess.run(["prefiq", "--help"], capture_output=True, text=True)
        if result.returncode == 0:
            print("[OK] prefiq CLI installed successfully!")
            print("→", result.stdout.splitlines()[0])
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
    # Step 1: Clone repo
    if not PROJECT_DIR.exists():
        print(f"[+] Cloning repository into {PROJECT_DIR}...")
        run_command(f"git clone --depth 1 {REPO_URL} {PROJECT_DIR}")
    else:
        print(f"[✔] Repository already exists at {PROJECT_DIR}")

    os.chdir(PROJECT_DIR)
    print(f"[✔] Changed working directory to {PROJECT_DIR}")

    # Step 2: Initialize npm if needed
    if not (PROJECT_DIR / "package.json").exists():
        print("[+] Initializing npm project...")
        run_command("npm init -y")
    else:
        print("[✔] npm already initialized.")

    # Step 3: System requirements
    print("[✔] Python already running...")

    check_and_install_package("Node.js", "node -v",
        "curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash - && sudo apt-get install -y nodejs")
    check_and_install_package("npm", "npm -v", "sudo apt-get install -y npm")
    check_and_install_package("Yarn", "yarn -v", "npm install -g yarn")
    check_and_install_package("Vite", "vite -v", "npm install -g vite")
    check_and_install_package("Concurrently", "concurrently --version", "npm install -g concurrently")

    # Step 4: Install Python & frontend deps
    print("[+] Installing Python requirements...")
    run_command(f"{sys.executable} -m pip install --no-cache-dir -r requirements.txt")

    print("[+] Installing frontend npm packages...")
    run_command("npm install")

    # Step 5: Install CLI in editable mode
    install_prefiq_editable()
    verify_prefiq_installation()

    print("[+] Installing assets for backend...")
    run_command(" npm run build:cortex")

    # Step 6: Build or run
    if MODE == "prod":
        print("[+] Building frontend for production...")
        run_command("npm run build")

        print("[🚀] Starting FastAPI backend in production...")
        run_command("gunicorn cortex.main:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:5005 -w 4 --timeout 60")
    else:
        print("[🚀] Starting backend and frontend in development...")
        run_command(
            'concurrently "uvicorn cortex.main:app --host 0.0.0.0 --port 5005 --reload" '
            '"npm run dev -- --host 0.0.0.0 --port 3005"'
        )


if __name__ == "__main__":
    main()
