from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from cortex.DTO.dal import Base


class Blog(Base):
    __tablename__ = "blog"

    id = Column(Integer, primary_key=True, index=True)
    blog_title = Column(String(128), index=True)
    blog_image = Column(String(256))  # Increased size to accommodate full URLs
    blog_description = Column(Text)  # Changed to Text for long content
    blog_author = Column(String(128))
    blog_category = Column(String(128))
    blog_tags = Column(String(256))  # Tags as comma-separated string
    blog_post_date = Column(DateTime, default=datetime.utcnow)
