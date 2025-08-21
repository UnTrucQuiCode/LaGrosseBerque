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
    
    