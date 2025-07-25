# prefiq/commands/git/update.py

import typer

from prefiq.github.git_sync import sync_repo

git_sync = typer.Typer(help="Git-related commands")

@git_sync.command("update")
def update_cmd():
    """Sync the local repo with remote (pull, commit, push)"""
    try:
        result = sync_repo()
        for key, val in result.items():
            print(f"{key.upper()}:\n{val}\n")
    except Exception as e:
        print(f"❌ Error: {e}")
