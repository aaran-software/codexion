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
