from pydantic import BaseModel
from datetime import datetime

class ReceiptCreate(BaseModel):
    acc_book: str
    date:datetime
    party_name: str
    amount: int
    transaction_type: str
    remarks: str

class ReceiptUpdate(BaseModel):
    acc_book: str
    date: datetime
    party_name: str
    amount: int
    transaction_type: str
    remarks: str

class Receipt(BaseModel):  # renamed from SaleOut for consistency
    id: int
    acc_book: str
    date: datetime
    party_name: str
    amount: int
    transaction_type: str
    remarks: str
    created_at: datetime

    class Config:
        orm_mode = True
