from sqlmodel import SQLModel, Field
from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime

class Souvenir(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    type: str
    contenu: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    poids: float = 1.0
    tags: List[str] = Field(default_factory=list, sa_column_kwargs={"type_": "TEXT"})  # converti à la main

    class Config:
        arbitrary_types_allowed = True
