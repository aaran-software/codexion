from sqlalchemy import Column, String
from cortex.DTO.dal import Base

class Blog(Base):
    __tablename__ = 'blog'
    id: str
    blog_title: str
    blog_image: str
    blog_description: str
    blog_author: str
    blog_category: str
    blog_tags: str
    blog_post_date: str
