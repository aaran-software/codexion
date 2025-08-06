from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List

from apps.cxsun.core.database.schemas import payment_schema
from apps.cxsun.core.models.Payment import Payment
from cortex.DTO.dal import get_db

router = APIRouter(prefix="/payment", tags=["Payment"])

# Create payment
@router.post("/", response_model=List[payment_schema.Payment])
async def create_payments(
    request: Request,
    db: Session = Depends(get_db)
):
    data = await request.json()

    if isinstance(data, dict):
        data = [data]  # wrap single item into a list

    payments = [payment_schema.PaymentCreate(**item) for item in data]
    db_payments = [Payment(**payment.dict()) for payment in payments]

    db.add_all(db_payments)
    db.commit()
    for payment in db_payments:
        db.refresh(payment)
    return db_payments

# Read single payment
@router.get("/{payment_id}", response_model=payment_schema.Payment)
def read_payment(payment_id: int, db: Session = Depends(get_db)):
    db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="payment not found")
    return db_payment

# Read all payments
@router.get("/", response_model=List[payment_schema.Payment])
def read_payments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Payment).offset(skip).limit(limit).all()

# Update payment
@router.put("/{payment_id}", response_model=payment_schema.Payment)
def update_payment(
    payment_id: int,
    payment_data: payment_schema.PaymentUpdate,
    db: Session = Depends(get_db)
):
    db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="payment not found")

    for key, value in payment_data.dict().items():
        setattr(db_payment, key, value)

    db.commit()
    db.refresh(db_payment)
    return db_payment

# Delete payment
@router.delete("/{payment_id}", response_model=payment_schema.Payment)
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="payments not found")

    db.delete(db_payment)
    db.commit()
    return db_payment
