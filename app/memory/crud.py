"""CRUD operations for :class:`Souvenir` objects."""

from __future__ import annotations

from typing import Dict, List, Optional

from sqlmodel import select

from app.models.souvenir import Souvenir
from app.memory.db import get_session


def creer_souvenir(souvenir: Souvenir) -> Souvenir:
    """Persist a new :class:`Souvenir` in the database."""
    with get_session() as session:
        session.add(souvenir)
        session.commit()
        session.refresh(souvenir)
        return souvenir


def obtenir_souvenir(mem_id: int) -> Optional[Souvenir]:
    """Fetch a souvenir by its identifier."""
    with get_session() as session:
        return session.get(Souvenir, mem_id)


def chercher_souvenirs(limit: int = 10) -> List[Souvenir]:
    """Return a list of souvenirs ordered by recency."""
    with get_session() as session:
        statement = select(Souvenir).order_by(Souvenir.time.desc()).limit(limit)
        return list(session.exec(statement))


def mettre_a_jour_souvenir(mem_id: int, data: Dict) -> Optional[Souvenir]:
    """Update fields of an existing souvenir."""
    with get_session() as session:
        souvenir = session.get(Souvenir, mem_id)
        if not souvenir:
            return None
        for key, value in data.items():
            setattr(souvenir, key, value)
        session.add(souvenir)
        session.commit()
        session.refresh(souvenir)
        return souvenir


def supprimer_souvenir(mem_id: int) -> bool:
    """Remove a souvenir from the database."""
    with get_session() as session:
        souvenir = session.get(Souvenir, mem_id)
        if not souvenir:
            return False
        session.delete(souvenir)
        session.commit()
        return True


def enregistrer_souvenir(souvenir: Souvenir) -> Souvenir:
    """Convenience wrapper for :func:`creer_souvenir`."""
    return creer_souvenir(souvenir)

