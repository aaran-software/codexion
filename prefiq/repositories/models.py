from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field

class User(BaseModel):
    id: Optional[int] = Field(default=None)
    email: str
    name: str
    is_active: bool = True
