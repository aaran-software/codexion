import os
from pathlib import Path

# Define base structure
BASE_DIR = Path("../prefiq")
GIT_DIR = BASE_DIR / "git"
CMD_DIR = BASE_DIR / "commands" / "git"

# Ensure folders exist
GIT_DIR.mkdir(parents=True, exist_ok=True)
CMD_DIR.mkdir(parents=True, exist_ok=True)

# Create git_actions.py
git_actions_path = GIT_DIR / "git_actions.py"
if not git_actions_path.exists():
    git_actions_path.write_text("""# Auto-generated Git actions loader
import typer
from prefiq.commands.git import (
    connect, ssh, commit, push, pull, sync, status
)

app = typer.Typer(name="git", help="Git management for installed apps")

app.command()(connect.run)
app.command()(ssh.run)
app.command()(commit.run)
app.command()(push.run)
app.command()(pull.run)
app.command()(sync.run)
app.command()(status.run)

def attach_git_commands(parent_app):
    parent_app.add_typer(app, name="git")
""", encoding="utf-8")

# Command file template
def command_template(name: str, body: str) -> str:
    return f'''import typer
from pathlib import Path
from prefiq.utils.ui import print_success, print_warning

def run(
    app: str = typer.Argument(..., help="App name")
):
    {body.strip()}
'''

# Git commands and their initial (mock) logic
commands = {
    "connect.py": 'print_success("[OK] SSH key connected (mocked)")',
    "ssh.py": 'print_success("[OK] SSH key created and stored (mocked)")',
    "commit.py": 'print_success(f"[OK] Committed changes for {app} (mocked)")',
    "push.py": 'print_success(f"[OK] Pushed changes for {app} (mocked)")',
    "pull.py": 'print_success(f"[OK] Pulled latest for {app} (mocked)")',
    "sync.py": 'print_success(f"[OK] Synced {app} (pull → commit → push) (mocked)")',
    "status.py": 'print_success(f"[OK] Status for {app}: clean (mocked)")',
}

# Write command files with UTF-8 encoding
for file_name, body in commands.items():
    fpath = CMD_DIR / file_name
    if not fpath.exists():
        fpath.write_text(command_template(file_name.replace(".py", ""), body), encoding="utf-8")

print("[OK] Git folders and command files generated successfully.")
