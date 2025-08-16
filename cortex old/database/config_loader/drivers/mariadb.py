# core/database/config_loader/drivers/mariadb.py
def get_config(ctx) -> dict:
    return {
        "user": ctx.user,
        "password": ctx.password,
        "host": ctx.host,
        "port": ctx.port,
        "database": ctx.database,
        "pool_name": "default_async_pool",
        "pool_size": ctx.pool_size,
        "autocommit": ctx.autocommit,
    }
