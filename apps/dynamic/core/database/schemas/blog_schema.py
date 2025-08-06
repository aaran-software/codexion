from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BlogCreate(BaseModel):
    blog_title: str
    blog_image: str
    blog_description: str
    blog_author: str
    blog_category: str
    blog_tags: str
    blog_post_date: str

class BlogUpdate(BaseModel):
    blog_title: str
    blog_image: str
    blog_description: str
    blog_author: str
    blog_category: str
    blog_tags: str
    blog_post_date: str

class Blog(BaseModel):
    id: str
    blog_title: str
    blog_image: str
    blog_description: str
    blog_author: str
    blog_category: str
    blog_tags: str
    blog_post_date: str
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
