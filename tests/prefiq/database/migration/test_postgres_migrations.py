# tests/test_postgres_migrations.py
from __future__ import annotations
import pytest

from tests.conftest import assert_migrations_table


@pytest.mark.postgres
def test_postgres_migrations_table_exists(postgres_env):
    """
    Boots the app on Postgres and verifies MigrationProvider created 'migrations'.
    """
    assert_migrations_table()
