import os
import subprocess
from cortex.core.settings import get_settings

class GitSync:
    def __init__(self):
        settings = get_settings()
        self.repo_path = settings.git_url

        # 🔒 Validate repo path
        if not os.path.isdir(self.repo_path):
            raise ValueError(f"Invalid repo path: {self.repo_path}")

    def run_git_command(self, *args):
        try:
            result = subprocess.run(
                ["git", *args],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return {"success": True, "output": result.stdout.strip()}
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": e.stderr.strip()}

    def sync(self):
        return self.run_git_command("pull")
