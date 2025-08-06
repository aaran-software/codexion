from pydantic import BaseModel
from datetime import datetime

class SaleCreate(BaseModel):
    item_name: str
    category: str
    quantity: int
    price: float

class SaleUpdate(BaseModel):
    item_name: str
    category: str
    quantity: int
    price: float

class Sale(BaseModel):  # renamed from SaleOut for consistency
    id: int
    item_name: str
    category: str
    quantity: int
    price: float
    created_at: datetime

    class Config:
        orm_mode = True
