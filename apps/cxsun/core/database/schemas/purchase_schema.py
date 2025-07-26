from pydantic import BaseModel
from datetime import datetime

class PurchaseCreate(BaseModel):
    item_name: str
    quantity: int
    price: float

class PurchaseUpdate(BaseModel):
    item_name: str
    quantity: int
    price: float

class Purchase(BaseModel):  # renamed from PurchaseOut for consistency
    id: int
    item_name: str
    quantity: int
    price: float
    created_at: datetime

    class Config:
        orm_mode = True
