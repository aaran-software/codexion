# tests/conftest.py
from __future__ import annotations
import os
import uuid
import contextlib
import pytest

from prefiq.settings.get_settings import clear_settings_cache
from prefiq.database.connection import reload_engine_from_env, reset_engine


def _restore_env(snapshot: dict[str, str | None]) -> None:
    for k, v in snapshot.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v

@pytest.fixture(scope="function")
def engine_swap():
    snaps: dict[str, str | None] = {}
    keys = ["DB_ENGINE", "DB_MODE", "DB_HOST", "DB_PORT", "DB_USER", "DB_PASS", "DB_NAME"]
    for k in keys:
        snaps[k] = os.environ.get(k)

    @contextlib.contextmanager
    def _ctx(**overrides):
        try:
            for k, v in overrides.items():
                os.environ[k] = str(v)
            clear_settings_cache()
            reset_engine()
            reload_engine_from_env(force_refresh=True)
            yield
        finally:
            _restore_env(snaps)
            clear_settings_cache()
            reset_engine()
            reload_engine_from_env(force_refresh=True)

    return _ctx

@pytest.fixture()
def unique_table():
    return f"ut_{uuid.uuid4().hex[:10]}"

# ---- Test helper expected by tests/prefiq/test_boot_doctor.py ----

class DummySettings:
    # sensible defaults for tests
    ENV = "test"
    TESTING = True

    DB_ENGINE = "sqlite"
    DB_MODE = "sync"
    DB_HOST = "localhost"
    DB_PORT = 0
    DB_USER = ""
    DB_PASS = ""
    DB_NAME = ":memory:"
    DB_POOL_WARMUP = 0

    JWT_SECRET_KEY = "dummy"
    JWT_ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60

    LOG_LEVEL = "DEBUG"
    LOG_FORMAT = "text"
    LOG_NAMESPACE = "prefiq"
    LOG_COLOR = "auto"

    DB_CLOSE_ATEXIT = True

    # optional app-ish fields some checks might read
    app_name = "TEST_APP"
    app_env = "test"
    app_port = "0"
    app_debug = "true"
    app_url = "http://localhost"
    app_title = "TEST_APP"

    def dsn(self) -> str:
        # sqlite DSN style used in doctor output
        return f"sqlite:///{self.DB_NAME}"
