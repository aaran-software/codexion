from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List

from apps.cxsun.core.database.schemas import purchase_schema
from apps.cxsun.core.models.Purchase import Purchase
from cortex.DTO.dal import get_db

router = APIRouter(prefix="/purchases", tags=["Purchases"])

# Create Purchase
@router.post("/", response_model=List[purchase_schema.Purchase])
async def create_purchases(
    request: Request,
    db: Session = Depends(get_db)
):
    data = await request.json()

    if isinstance(data, dict):
        data = [data]  # wrap single item into a list

    purchases = [purchase_schema.PurchaseCreate(**item) for item in data]
    db_purchases = [Purchase(**purchase.dict()) for purchase in purchases]

    db.add_all(db_purchases)
    db.commit()
    for purchase in db_purchases:
        db.refresh(purchase)
    return db_purchases

# Read single Purchase
@router.get("/{purchase_id}", response_model=purchase_schema.Purchase)
def read_purchase(purchase_id: int, db: Session = Depends(get_db)):
    db_purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
    if not db_purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return db_purchase

# Read all Purchases
@router.get("/", response_model=List[purchase_schema.Purchase])
def read_purchases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Purchase).offset(skip).limit(limit).all()

# Update Purchase
@router.put("/{purchase_id}", response_model=purchase_schema.Purchase)
def update_purchase(
    purchase_id: int,
    purchase_data: purchase_schema.PurchaseUpdate,
    db: Session = Depends(get_db)
):
    db_purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
    if not db_purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")

    for key, value in purchase_data.dict().items():
        setattr(db_purchase, key, value)

    db.commit()
    db.refresh(db_purchase)
    return db_purchase

# Delete Purchase
@router.delete("/{purchase_id}", response_model=purchase_schema.Purchase)
def delete_purchase(purchase_id: int, db: Session = Depends(get_db)):
    db_purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
    if not db_purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")

    db.delete(db_purchase)
    db.commit()
    return db_purchase
