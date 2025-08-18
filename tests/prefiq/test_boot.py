from prefiq.core.runtime.bootstrap import main
from prefiq.core.contracts.base_provider import Application
from prefiq.database.engines.mariadb.health import is_healthy

def test_boot_and_bindings():
    main()
    app = Application.get_app()
    assert app.resolve("settings") is not None
    assert app.resolve("profiles") is not None
    db = app.resolve("db")
    assert db is not None
    assert is_healthy(db) is True

def test_simple_query():
    app = Application.get_app()
    db = app.resolve("db")
    assert db.fetchone("SELECT 1") is not None
