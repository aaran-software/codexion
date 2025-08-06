# cortex/database/pool.py

import mariadb
from contextlib import asynccontextmanager
from anyio.to_thread import run_sync

_pool_config = None


db_config = {
    "user": "root",
    "password": "secret",
    "host": "127.0.0.1",
    "port": 3306,
    "database": "your_db_name",
}

def init_pool(config):
    global _pool_config
    _pool_config = config


@asynccontextmanager
async def get_connection():
    if _pool_config is None:
        raise Exception("Pool not initialized. Call init_pool(config) first.")

    def get_conn_cursor():
        conn = mariadb.connect(**_pool_config)
        cur = conn.cursor()
        return conn, cur

    conn, cur = await run_sync(get_conn_cursor)
    try:
        yield cur
        await run_sync(conn.commit)
    finally:
        await run_sync(cur.close)
        await run_sync(conn.close)


async def close_pool():
    # No-op for thread-based connections
    pass
