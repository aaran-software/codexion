from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List

from apps.dynamic.core.database.schemas import blog_schema
from apps.dynamic.core.models.blog import Blog
from cortex.DTO.dal import get_db

router = APIRouter(prefix='/blog', tags=['blog'])

@router.post('/', response_model=List[blog_schema.Blog])
async def create_items(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    if isinstance(data, dict):
        data = [data]
    items = [blog_schema.BlogCreate(**item) for item in data]
    db_items = [Blog(**item.dict()) for item in items]
    db.add_all(db_items)
    db.commit()
    for item in db_items:
        db.refresh(item)
    return db_items

@router.get('/{item_id}', response_model=blog_schema.Blog)
def read_item(item_id: str, db: Session = Depends(get_db)):
    item = db.query(Blog).filter(Blog.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail='Item not found')
    return item

@router.get('/', response_model=List[blog_schema.Blog])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Blog).offset(skip).limit(limit).all()

@router.put('/{item_id}', response_model=blog_schema.Blog)
def update_item(item_id: str, data: blog_schema.BlogUpdate, db: Session = Depends(get_db)):
    db_item = db.query(Blog).filter(Blog.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail='Item not found')
    for key, value in data.dict(exclude_unset=True).items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete('/{item_id}', response_model=blog_schema.Blog)
def delete_item(item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(Blog).filter(Blog.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail='Item not found')
    db.delete(db_item)
    db.commit()
    return db_item
