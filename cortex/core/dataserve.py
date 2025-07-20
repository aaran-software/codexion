# cortex/core/dataserve.py

def get_database_url():
    from cortex.core.config import get_settings  # moved inside function

    settings = get_settings()
    db_engine = settings.DB_ENGINE.lower()

    if db_engine == "sqlite":
        db_name = settings.DB_NAME
        if not db_name.endswith(".db"):
            db_name += ".db"
        return f"sqlite:///{db_name}"

    if db_engine == "mysql":
        return f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

    if db_engine == "postgresql":
        return f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

    raise ValueError(f"Unsupported DB_ENGINE: {db_engine}")
