from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime

from cortex.DTO.dal import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_title = Column(String(128), index=True)
    task_description = Column(Text, index=True)  # allows very long text
    user_id = Column(Integer, ForeignKey("users.id"))  # foreign key to users table
    created_at = Column(DateTime, default=datetime.utcnow)
