from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, DateTime, JSON, Date
from cortex.DTO.dal import Base

from typing import List
from datetime import datetime, date

class Blog(Base):
    __tablename__ = 'blog'

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    blog_title: Mapped[str] = mapped_column(String(255))
    blog_image: Mapped[str] = mapped_column(String(255))
    blog_description: Mapped[str] = mapped_column(String(255))
    blog_author: Mapped[str] = mapped_column(String(255))
    blog_category: Mapped[str] = mapped_column(String(255))
    blog_tags: Mapped[str] = mapped_column(String(255))
    blog_post_date: Mapped[date] = mapped_column(Date)
