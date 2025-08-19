# prefiq/database/connection_manager.py
from contextlib import contextmanager, asynccontextmanager
from prefiq.database.connection import get_engine

class ConnectionManager:
    def __init__(self):
        pass

    def get_engine(self):
        return get_engine()

    def test(self) -> bool:
        return self.get_engine().test_connection()

    @contextmanager
    def transaction(self):
        eng = self.get_engine()
        try:
            eng.begin()
            yield eng
            eng.commit()
        except Exception:
            eng.rollback()
            raise

    @asynccontextmanager
    async def transaction_async(self):
        eng = self.get_engine()
        try:
            await eng.begin()
            yield eng
            await eng.commit()
        except Exception:
            await eng.rollback()
            raise

    def close(self):
        self.get_engine().close()

connection_manager = ConnectionManager()
