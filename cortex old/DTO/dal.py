# cortex/DTO/dal.py

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from cortex.core.settings import get_settings

settings = get_settings()
engine = create_engine(settings.database_url, echo=True)

# ← single source of truth for models metadata
Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()