# tests/conftest.py
import asyncio, inspect
import pytest
from prefiq.core.contracts.base_provider import Application

@pytest.fixture(scope="session", autouse=True)
def boot_and_close():
    from prefiq.core.runtime.bootstrap import main
    main()
    yield
    db = Application.get_app().resolve("db")
    if hasattr(db, "close"):
        res = db.close()
        if inspect.isawaitable(res):
            asyncio.run(res)
