# app/memory/crud.py

from app.memory.models import Souvenir
from app.memory.db import get_session
from typing import List
from sqlmodel import select

def creer_souvenir(s: Souvenir) -> Souvenir:
    with get_session() as session:
        session.add(s)
        session.commit()
        session.refresh(s)
        return s

def chercher_souvenirs(limit: int = 10) -> List[Souvenir]:
    with get_session() as session:
        statement = select(Souvenir).order_by(Souvenir.timestamp.desc()).limit(limit)
        return list(session.exec(statement))
