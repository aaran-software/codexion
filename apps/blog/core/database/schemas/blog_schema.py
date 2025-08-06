from datetime import datetime

from pydantic import BaseModel

class BlogCreate(BaseModel):
    blog_title: str
    blog_image: str
    blog_description: str
    blog_author: str
    blog_category: str
    blog_tags: str
    blog_post_date:datetime

class BlogUpdate(BaseModel):
    blog_title: str
    blog_image: str
    blog_description: str
    blog_author: str
    blog_category: str
    blog_tags: str
    blog_post_date: datetime

class Blog(BaseModel):  # renamed from SaleOut for consistency
    id: int
    blog_title: str
    blog_image: str
    blog_description: str
    blog_author: str
    blog_category: str
    blog_tags: str
    blog_post_date: datetime

    class Config:
        orm_mode = True
