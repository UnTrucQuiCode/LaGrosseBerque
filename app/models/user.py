from typing import Optional
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    permissions: Optional[str] = default
    type: str """AI or human"""