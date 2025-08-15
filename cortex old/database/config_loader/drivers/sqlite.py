# core/database/config_loader/drivers/sqlite.py
def get_config(ctx) -> dict:
    return {
        "database": ctx.database or ":memory:"
    }
