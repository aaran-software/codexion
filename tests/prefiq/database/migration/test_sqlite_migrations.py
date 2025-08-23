# tests/test_sqlite_migrations.py
from __future__ import annotations

from tests.conftest import assert_migrations_table  # re-use helper


def test_sqlite_migrations_table_exists(sqlite_env):
    """
    Boots the app on SQLite and verifies MigrationProvider created 'migrations'.
    """
    assert_migrations_table()
