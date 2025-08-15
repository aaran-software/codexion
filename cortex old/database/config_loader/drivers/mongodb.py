# core/database/config_loader/drivers/mongodb.py
def get_config(ctx) -> dict:
    # MongoDB is URI-based, optionally build one if not provided
    if ctx.uri:
        return {"uri": ctx.uri}

    user_pass = f"{ctx.user}:{ctx.password}@" if ctx.user and ctx.password else ""
    uri = f"mongodb://{user_pass}{ctx.host}:{ctx.port}/{ctx.database}"
    return {
        "uri": uri,
        "database": ctx.database
    }
