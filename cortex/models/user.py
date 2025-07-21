# cortex/models/user.py
from sqlalchemy import Column, Integer, String, DateTime
from cortex.DTO.dal import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(512), nullable=False)  # store hashed passwords
    created_at = Column(DateTime, default=datetime.utcnow)
