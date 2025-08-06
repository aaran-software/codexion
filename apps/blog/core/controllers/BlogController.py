from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List

from apps.blog.core.database.schemas import blog_schema
from apps.blog.core.models.Blog import Blog
from cortex.DTO.dal import get_db

router = APIRouter(prefix="/blog", tags=["blog"])

# Create blog
@router.post("/", response_model=List[blog_schema.Blog])
async def create_blogs(
    request: Request,
    db: Session = Depends(get_db)
):
    data = await request.json()

    if isinstance(data, dict):
        data = [data]  # wrap single item into a list

    blogs = [blog_schema.BlogCreate(**item) for item in data]
    db_blogs = [Blog(**blog.dict()) for blog in blogs]

    db.add_all(db_blogs)
    db.commit()
    for blog in db_blogs:
        db.refresh(blog)
    return db_blogs

# Read single blog
@router.get("/{blog_id}", response_model=blog_schema.Blog)
def read_blog(blog_id: int, db: Session = Depends(get_db)):
    db_blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not db_blog:
        raise HTTPException(status_code=404, detail="blog not found")
    return db_blog

# Read all blogs
@router.get("/", response_model=List[blog_schema.Blog])
def read_blogs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Blog).offset(skip).limit(limit).all()

# Update blog
@router.put("/{blog_id}", response_model=blog_schema.Blog)
def update_blog(
    blog_id: int,
    blog_data: blog_schema.BlogUpdate,
    db: Session = Depends(get_db)
):
    db_blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not db_blog:
        raise HTTPException(status_code=404, detail="blog not found")

    for key, value in blog_data.dict().items():
        setattr(db_blog, key, value)

    db.commit()
    db.refresh(db_blog)
    return db_blog

# Delete blog
@router.delete("/{blog_id}", response_model=blog_schema.Blog)
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    db_blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not db_blog:
        raise HTTPException(status_code=404, detail="blogs not found")

    db.delete(db_blog)
    db.commit()
    return db_blog
