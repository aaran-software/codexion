# tests/conftest.py
from __future__ import annotations

import os
import uuid
import contextlib
import pytest

# Fast, safe defaults for the whole test session
os.environ.setdefault("TESTING", "1")
os.environ.setdefault("DB_ENGINE", "sqlite")
os.environ.setdefault("DB_MODE", "sync")
os.environ.setdefault("DB_NAME", ":memory:")

from prefiq.settings.get_settings import clear_settings_cache
from prefiq.database.connection import get_engine, reset_engine, reload_engine_from_env


def _restore_env(snapshot: dict[str, str | None]) -> None:
    for k, v in snapshot.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v


@pytest.fixture(scope="function")
def engine_swap():
    """
    Context-manager fixture that temporarily overrides DB_* env vars,
    resets the settings cache + engine singleton, and restores on exit.
    """
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


def pytest_configure(config):
    # Register markers to avoid PytestUnknownMarkWarning
    config.addinivalue_line("markers", "postgres: requires a running Postgres instance")
    config.addinivalue_line("markers", "mariadb: requires a running MariaDB instance")


# --- CLI options for DBs (runtime, no .env needed) ---
def pytest_addoption(parser):
    grp = parser.getgroup("db")

    # Postgres
    grp.addoption("--pg-host", action="store", default="127.0.0.1")
    grp.addoption("--pg-port", action="store", type=int, default=5432)
    grp.addoption("--pg-user", action="store", default="postgres")
    grp.addoption("--pg-pass", action="store", default="DbPass1@@")
    grp.addoption("--pg-db",   action="store", default="prefiq_dev")
    grp.addoption("--pg-mode", action="store", default="sync", choices=["sync", "async"])

    # MariaDB (mirror PG so it runs w/o .env)
    grp.addoption("--mysql-host", action="store", default="127.0.0.1")
    grp.addoption("--mysql-port", action="store", type=int, default=3306)
    grp.addoption("--mysql-user", action="store", default="root")
    grp.addoption("--mysql-pass", action="store", default="Computer.1")
    grp.addoption("--mysql-db",   action="store", default="codexion_db")
    grp.addoption("--mysql-mode", action="store", default="sync", choices=["sync", "async"])


# Structured configs built from CLI flags (always present thanks to defaults)
@pytest.fixture(scope="session")
def pg_cli(pytestconfig):
    return {
        "host": pytestconfig.getoption("--pg-host"),
        "port": pytestconfig.getoption("--pg-port"),
        "user": pytestconfig.getoption("--pg-user"),
        "password": pytestconfig.getoption("--pg-pass"),
        "db": pytestconfig.getoption("--pg-db"),
        "mode": (pytestconfig.getoption("--pg-mode") or "sync").lower(),
    }


@pytest.fixture(scope="session")
def mysql_cli(pytestconfig):
    return {
        "host": pytestconfig.getoption("--mysql-host"),
        "port": pytestconfig.getoption("--mysql-port"),
        "user": pytestconfig.getoption("--mysql-user"),
        "password": pytestconfig.getoption("--mysql-pass"),
        "db": pytestconfig.getoption("--mysql-db"),
        "mode": (pytestconfig.getoption("--mysql-mode") or "sync").lower(),
    }
