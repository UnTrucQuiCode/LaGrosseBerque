from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class Souvenir(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    auteur: str
    contenu: str
    contexte: Optional[str] = None
    date: datetime = Field(default_factory=datetime.now)
    importance_globale: float = 0.5
