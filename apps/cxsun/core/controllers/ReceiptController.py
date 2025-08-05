from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List

from apps.cxsun.core.database.schemas import receipt_schema
from apps.cxsun.core.models.Receipt import Receipt
from cortex.DTO.dal import get_db

router = APIRouter(prefix="/receipt", tags=["Receipt"])

# Create receipt
@router.post("/", response_model=List[receipt_schema.Receipt])
async def create_receipts(
    request: Request,
    db: Session = Depends(get_db)
):
    data = await request.json()

    if isinstance(data, dict):
        data = [data]  # wrap single item into a list

    receipts = [receipt_schema.ReceiptCreate(**item) for item in data]
    db_receipts = [Receipt(**receipt.dict()) for receipt in receipts]

    db.add_all(db_receipts)
    db.commit()
    for receipt in db_receipts:
        db.refresh(receipt)
    return db_receipts

# Read single receipt
@router.get("/{receipt_id}", response_model=receipt_schema.Receipt)
def read_receipt(receipt_id: int, db: Session = Depends(get_db)):
    db_receipt = db.query(Receipt).filter(Receipt.id == receipt_id).first()
    if not db_receipt:
        raise HTTPException(status_code=404, detail="receipt not found")
    return db_receipt

# Read all receipts
@router.get("/", response_model=List[receipt_schema.Receipt])
def read_receipts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Receipt).offset(skip).limit(limit).all()

# Update receipt
@router.put("/{receipt_id}", response_model=receipt_schema.Receipt)
def update_receipt(
    receipt_id: int,
    receipt_data: receipt_schema.ReceiptUpdate,
    db: Session = Depends(get_db)
):
    db_receipt = db.query(Receipt).filter(Receipt.id == receipt_id).first()
    if not db_receipt:
        raise HTTPException(status_code=404, detail="receipt not found")

    for key, value in receipt_data.dict().items():
        setattr(db_receipt, key, value)

    db.commit()
    db.refresh(db_receipt)
    return db_receipt

# Delete receipt
@router.delete("/{receipt_id}", response_model=receipt_schema.Receipt)
def delete_receipt(receipt_id: int, db: Session = Depends(get_db)):
    db_receipt = db.query(Receipt).filter(Receipt.id == receipt_id).first()
    if not db_receipt:
        raise HTTPException(status_code=404, detail="receipts not found")

    db.delete(db_receipt)
    db.commit()
    return db_receipt
