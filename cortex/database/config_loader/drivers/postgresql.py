# core/database/config_loader/drivers/postgresql.py
def get_config(ctx) -> dict:
    return {
        "user": ctx.user,
        "password": ctx.password,
        "host": ctx.host,
        "port": ctx.port,
        "dbname": ctx.database,
        "sslmode": "prefer"
    }
