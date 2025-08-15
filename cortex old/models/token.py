
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
import datetime
from cortex.DTO.dal import Base


class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(512), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    expired = Column(Boolean, default=False)