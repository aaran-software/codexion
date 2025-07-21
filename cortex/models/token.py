# # apps/models/token.py
# from sqlalchemy import Column, Integer, String, DateTime, Boolean
# from  cortex.DTO import DAL
#
#
# class Token(DAL):
#     __tablename__ = "tokens"
#
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, index=True)
#     token = Column(String, unique=True, index=True)
#     expires_at = Column(DateTime)
#     is_valid = Column(Boolean, default=True)

from sqlalchemy import Column, Integer, String, DateTime, Boolean
import datetime
from cortex.DTO.dal import Base


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(512), unique=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    expired = Column(Boolean, default=False)
