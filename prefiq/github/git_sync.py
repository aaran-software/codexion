import os
import subprocess

REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # root of repo
BRANCH = "main"


def run(cmd, cwd=REPO_DIR):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}\n{result.stderr}")
    return result.stdout.strip()


def pull_repo():
    return run(f"git pull origin {BRANCH}")


def push_repo(commit_message="sync: update via API or script"):
    run("git add .")
    run(f'git commit -m "{commit_message}"')
    return run(f"git push origin {BRANCH}")


def sync_repo():
    output = {}
    output["pull"] = pull_repo()

    status = run("git status --porcelain")
    if status:
        output["push"] = push_repo()
        output["status"] = "✅ Changes committed and pushed"
    else:
        output["status"] = "✅ No changes to push"

    return output
