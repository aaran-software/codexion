from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List

from apps.cxsun.core.database.schemas import sales_schema
from apps.cxsun.core.models.Sales import Sales
from cortex.DTO.dal import get_db

router = APIRouter(prefix="/sales", tags=["Sales"])

# Create sale
@router.post("/", response_model=List[sales_schema.Sale])
async def create_sales(
    request: Request,
    db: Session = Depends(get_db)
):
    data = await request.json()

    if isinstance(data, dict):
        data = [data]  # wrap single item into a list

    sales = [sales_schema.SaleCreate(**item) for item in data]
    db_sales = [Sales(**sale.dict()) for sale in sales]

    db.add_all(db_sales)
    db.commit()
    for sale in db_sales:
        db.refresh(sale)
    return db_sales

# Read single sale
@router.get("/{sales_id}", response_model=sales_schema.Sale)
def read_sale(sales_id: int, db: Session = Depends(get_db)):
    db_sale = db.query(Sales).filter(Sales.id == sales_id).first()
    if not db_sale:
        raise HTTPException(status_code=404, detail="sale not found")
    return db_sale

# Read all sales
@router.get("/", response_model=List[sales_schema.Sale])
def read_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Sales).offset(skip).limit(limit).all()

# Update sale
@router.put("/{sales_id}", response_model=sales_schema.Sale)
def update_sale(
    sales_id: int,
    sale_data: sales_schema.SaleUpdate,
    db: Session = Depends(get_db)
):
    db_sale = db.query(Sales).filter(Sales.id == sales_id).first()
    if not db_sale:
        raise HTTPException(status_code=404, detail="sale not found")

    for key, value in sale_data.dict().items():
        setattr(db_sale, key, value)

    db.commit()
    db.refresh(db_sale)
    return db_sale

# Delete sale
@router.delete("/{sales_id}", response_model=sales_schema.Sale)
def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    db_sale = db.query(Sales).filter(Sales.id == sale_id).first()
    if not db_sale:
        raise HTTPException(status_code=404, detail="Sales not found")

    db.delete(db_sale)
    db.commit()
    return db_sale
