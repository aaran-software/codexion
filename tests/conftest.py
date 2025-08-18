# tests/conftest.py

import os
import pytest

from prefiq.settings.get_settings import clear_settings_cache


@pytest.fixture(autouse=True)
def reset_settings_env(monkeypatch):
    """
    This fixture runs before each test:
    - Sets TESTING=true
    - Clears cached settings
    - Lets you override env vars with monkeypatch
    """
    # Force fresh environment for every test
    monkeypatch.setenv("TESTING", "true")

    # Clear settings cache before test starts
    clear_settings_cache()

    yield

    # Optional: clear again after test
    clear_settings_cache()
