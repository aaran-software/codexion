from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from cortex.DTO.dal import Base


class Receipt(Base):
    __tablename__ = "receipt"


    id = Column(Integer, primary_key=True, index=True)
    acc_book = Column(String(128), index=True)
    date = Column(DateTime)
    party_name = Column(String(128), index=True)
    amount = Column(Integer)
    transaction_type = Column(String(128), index=True)
    remarks = Column(String(128), index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
