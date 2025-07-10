from sqlmodel import SQLModel, Field, Column
from sqlalchemy.types import TEXT
from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import List
import json

# --- Fonctions de sérialisation/désérialisation des tags ---

def serialize_tags(tags: List[str]) -> str:
    """
    Convertit une liste de tags en chaîne JSON pour stockage en base.
    """
    return json.dumps(tags)

def deserialize_tags(value: str) -> List[str]:
    """
    Convertit une chaîne JSON depuis la base en liste Python.
    """
    return json.loads(value)

# --- Modèle principal : Souvenir ---

class Souvenir(SQLModel, table=True):
    """
    Représente un souvenir dans la base de données.
    """

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    type: str                                 # Ex : "dialogue", "mémoire_longue", "système", etc.
    contenu: str                              # Le contenu textuel du souvenir
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )                                         # Date de création du souvenir (UTC)
    poids: float = 0.1                        # Pondération : importance ou intensité du souvenir

    # Les tags sont stockés en base comme une chaîne JSON,
    # mais accessibles comme une liste Python
    tags: List[str] = Field(
        default_factory=list,
        sa_column=Column(TEXT, default="[]")
    )

    def __init__(self, **kwargs):
        """
        Surcharge du constructeur pour sérialiser les tags automatiquement.
        """
        if "tags" in kwargs and isinstance(kwargs["tags"], list):
            kwargs["tags"] = serialize_tags(kwargs["tags"])
        super().__init__(**kwargs)

    def __post_init__(self):
        """
        Déserialisation automatique des tags après création de l'objet.
        (utile si on charge depuis la base avec SQLAlchemy)
        """
        if isinstance(self.tags, str):
            self.tags = deserialize_tags(self.tags)

    def get_tags(self) -> List[str]:
        """
        Méthode utilitaire pour récupérer les tags de façon sécurisée.
        """
        if isinstance(self.tags, str):
            return deserialize_tags(self.tags)
        return self.tags
