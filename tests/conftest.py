import os
import types
import pytest

@pytest.fixture(autouse=True)
def _ensure_testing_env(monkeypatch):
    # Make settings loader skip the global cache
    monkeypatch.setenv("TESTING", "1")
    yield

class DummySettings(types.SimpleNamespace):
    # Defaults used by the doctors
    ENV: str = "development"
    DB_ENGINE: str = "sqlite"
    DB_MODE: str = "sync"
    DB_HOST: str = "127.0.0.1"
    DB_NAME: str = ":memory:"
