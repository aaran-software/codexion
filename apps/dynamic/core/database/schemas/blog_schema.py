from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pymysql import Date

class BlogCreate(BaseModel):
    blog_title: str
    blog_image: str
    blog_description: str
    blog_author: str
    blog_category: str
    blog_tags: str
    blog_post_date: date

class BlogUpdate(BaseModel):
    blog_title: Optional[str] = None
    blog_image: Optional[str] = None
    blog_description: Optional[str] = None
    blog_author: Optional[str] = None
    blog_category: Optional[str] = None
    blog_tags: Optional[str] = None
    blog_post_date: Optional[date] = None

class Blog(BaseModel):
    id: str
    blog_title: str
    blog_image: str
    blog_description: str
    blog_author: str
    blog_category: str
    blog_tags: str
    blog_post_date: date
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
