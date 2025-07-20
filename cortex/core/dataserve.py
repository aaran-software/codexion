from pathlib import Path

def get_database_url():
    from cortex.core.config import get_settings
    settings = get_settings()

    db_engine = settings.DB_ENGINE.lower()

    if db_engine == "sqlite":
        db_name = settings.DB_NAME
        if not db_name.endswith(".db"):
            db_name += ".db"

        # Set path to root-level database/{db_name}
        project_root = Path(__file__).resolve().parent.parent.parent
        db_dir = project_root / "database"
        db_dir.mkdir(parents=True, exist_ok=True)

        db_path = db_dir / db_name

        return f"sqlite:///{db_path.as_posix()}"

    if db_engine == "mysql":
        return f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

    if db_engine == "postgresql":
        return f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

    raise ValueError(f"Unsupported DB_ENGINE: {db_engine}")
