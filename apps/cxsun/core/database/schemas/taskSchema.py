from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    task_title: str
    task_description: Optional[str] = None
    user_id: int

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    task_title: Optional[str] = None
    task_description: Optional[str] = None
    user_id: Optional[int] = None

class TaskOut(TaskBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
