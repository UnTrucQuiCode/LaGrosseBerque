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
    summary: Optional[str] = None
    content: str
    content_complete: Optional[str] = None
    author: str
    time: datetime = Field(default_factory=datetime.utcnow)
    weight: int = 0.1
    importance: int = 0.01
    Log_context: Optional[str] = None
    part_of: Optional[int] = None
    emotions: Optional[str] = None
    emotions_weight: int = 0
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
    activation_log: Optional[str] = None
    last_accessed: Optional[datetime] = None


class Link(SQLModel, table=True):
    """Description d'un lien mémorisable."""

    link_id: Optional[int] = Field(default=None, primary_key=True)
    type: str
    name: str
    description: str
    weight: int
    total_token: int


class LinkSouvenir(SQLModel, table=True):
    """Table d'association entre :class:`Souvenir` et :class:`Link`."""

    mem_id: int = Field(foreign_key="souvenir.mem_id", primary_key=True)
    link_id: int = Field(foreign_key="link.link_id", primary_key=True)


class EmoLvl2ToLv1(SQLModel, table=True):
    """Mapping des émotions de second niveau vers les émotions primaires."""

    __tablename__ = "emo_lvl2_to_lv1"

    emo_lvl2: str = Field(primary_key=True)
    joy: int = 0
    trust: int = 0
    fear: int = 0
    surprise: int = 0
    sadness: int = 0
    disgust: int = 0
    anger: int = 0
    anticipation: int = 0

