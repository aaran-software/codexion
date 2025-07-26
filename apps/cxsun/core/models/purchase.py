from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from cortex.DTO.dal import Base


class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String(128), index=True)
    quantity = Column(Integer)
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
