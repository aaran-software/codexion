# tests/conftest.py

import subprocess
import sys
import shutil
import os
import pytest
import json

APPS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "apps"))
TEST_APP = "testapp"
CONFIG_PATH = os.path.join(APPS_DIR, "config.json")

@pytest.fixture
def run_command():
    def _run(command: str):
        cmd = [sys.executable, "-u","-m", "prefiq"] + command.split()
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    return _run

@pytest.fixture(autouse=True)
def cleanup():
    # Let the test run
    yield

    # Remove testapp directory
    app_path = os.path.join(APPS_DIR, TEST_APP)
    if os.path.exists(app_path):
        shutil.rmtree(app_path)

    # Remove testapp entry from config
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                data = json.load(f)
            if TEST_APP in data.get("apps", []):
                data["apps"].remove(TEST_APP)
                with open(CONFIG_PATH, "w") as f:
                    json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Cleanup warning: {e}")
