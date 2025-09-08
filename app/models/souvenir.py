"""Model definition for souvenirs stored in the database."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Souvenir(SQLModel, table=True):
    """Representation d'un souvenir.

    Cette table est créée automatiquement si elle n'existe pas déjà
    grâce à :func:`sqlmodel.SQLModel.metadata.create_all`.
    """

    mem_id: Optional[int] = Field(default=None, primary_key=True)
    type: str
    summary: str = ""
    content: str
    content_complete: str
    author: str
    time: datetime = Field(default_factory=datetime.utcnow)
    weight: int = 0
    importance: int
    Log_context: str
    part_of: int
    emotions: str = ""
    tokens_content: int = 0
    tokens_summary: int = 0
    joy: int = 0
    trust: int = 0
    fear: int = 0
    surprise: int = 0
    sadness: int = 0
    disgust: int = 0  
    anger: int = 0
    anticipation: int = 0
    activation_log: str = ""
    last_accessed: Optional[datetime] = None

