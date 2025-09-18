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


class Fragment(SQLModel, table=True):
    """Fragment textuel conservé pour enrichir les contextes générés."""

    fragment_id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[int] = Field(default=None, foreign_key="user.user_id")


class Context(SQLModel, table=True):
    """Historique de contextes construits à partir de fragments."""

    context_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[int] = Field(default=None, foreign_key="user.user_id")


class BackgroundThought(SQLModel, table=True):
    """Réflexions de fond générées pour un contexte donné."""

    thought_id: Optional[int] = Field(default=None, primary_key=True)
    context_id: Optional[int] = Field(default=None, foreign_key="context.context_id")
    content: str
    confidence: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)


class WorkingMemory(SQLModel, table=True):
    """Éléments temporaires mis en avant pendant le raisonnement."""

    working_memory_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.user_id")
    fragment_id: Optional[int] = Field(default=None, foreign_key="fragment.fragment_id")
    state: str
    expires_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class User(SQLModel, table=True):
    """Profil utilisateur associé aux souvenirs et aux fragments."""

    user_id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    display_name: Optional[str] = None
    email: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

