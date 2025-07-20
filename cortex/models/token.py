# apps/models/token.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from  cortex.DTO.database import DAL


class Token(DAL):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    token = Column(String, unique=True, index=True)
    expires_at = Column(DateTime)
    is_valid = Column(Boolean, default=True)
