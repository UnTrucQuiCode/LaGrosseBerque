from typing import Optional
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    user_name: str = Field(default=None, primary_key=True)
    permissions: Optional[str] = 'default'
    type: str #AI or human"""
    is_active : bool = False