# cortex/DTO/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from cortex.core.config import get_settings

settings = get_settings()

engine = create_engine(settings.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
DAL = declarative_base()
