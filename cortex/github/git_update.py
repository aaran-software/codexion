import os
import subprocess
from cortex.core.settings import get_settings


class GitSync:
    def __init__(self):
        self.repo_path = get_settings().project_root

    def run_git_command(self, *args):
        try:
            result = subprocess.run(
                ["git", *args],
                cwd=self.repo_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return {"error": e.stderr.strip()}

    def sync(self):
        if not os.path.isdir(self.repo_path):
            return {"error": f"Invalid repo path: {self.repo_path}"}

        pull_output = self.run_git_command("pull")
        if isinstance(pull_output, dict) and "error" in pull_output:
            return pull_output

        last_commit = self.run_git_command("log", "-1", "--pretty=format:%h %s")
        return {
            "success": True,
            "updated_to": last_commit,
            "pull_output": pull_output,
        }
