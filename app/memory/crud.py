"""CRUD operations for memory models."""

from __future__ import annotations

from typing import Dict, List, Optional

from sqlalchemy import func
from sqlmodel import select

from app.models.memory import (
    Background_thought,
    Context,
    EmoLvl2ToLv1,
    Fragment,
    Link,
    LinkSouvenir,
    Souvenir,
    User,
    Working_memory,
)
from app.memory.db import get_session


def create_souvenir(souvenir: Souvenir) -> Souvenir:
    """Persist a new :class:`Souvenir` in the database."""
    with get_session() as session:
        if souvenir.souv_id is None:
            souvenir.souv_id = _next_souvenir_id(session, souvenir.user_name)
        session.add(souvenir)
        session.commit()
        session.refresh(souvenir)
        return souvenir

def _next_souvenir_id(session, user_name: Optional[str]) -> int:
    """Return the next souvenir identifier for the given user."""
    statement = select(func.coalesce(func.max(Souvenir.souv_id), 0) + 1)
    if user_name is not None:
        statement = statement.where(Souvenir.user_name == user_name)
    return session.exec(statement).one()



def get_souvenir(mem_id: int) -> Optional[Souvenir]:
    """Fetch a souvenir by its identifier."""
    with get_session() as session:
        return session.get(Souvenir, mem_id)


def seek_souvenirs(limit: int = 10) -> List[Souvenir]:
    """Return a list of souvenirs ordered by recency."""
    with get_session() as session:
        statement = select(Souvenir).order_by(Souvenir.time.desc()).limit(limit)
        return list(session.exec(statement))


def update_souvenir(mem_id: int, data: Dict) -> Optional[Souvenir]:
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


def delete_souvenir(mem_id: int) -> bool:
    """Remove a souvenir from the database."""
    with get_session() as session:
        souvenir = session.get(Souvenir, mem_id)
        if not souvenir:
            return False
        session.delete(souvenir)
        session.commit()
        return True


"""def save_souvenir(souvenir: Souvenir) -> Souvenir:
    # Convenience wrapper for :func:`create_souvenir`.
    return create_souvenir(souvenir)"""


# ----- CRUD pour la table emo_lvl2_to_lv1 -----

def create_emo_lvl2_to_lv1(mapping: EmoLvl2ToLv1) -> EmoLvl2ToLv1:
    """Persiste une nouvelle correspondance d'émotion de niveau 2."""
    with get_session() as session:
        session.add(mapping)
        session.commit()
        session.refresh(mapping)
        return mapping


def get_emo_lvl2_to_lv1(emo_lvl2: str) -> Optional[EmoLvl2ToLv1]:
    """Récupère une correspondance par son nom de niveau 2."""
    with get_session() as session:
        return session.get(EmoLvl2ToLv1, emo_lvl2)


def seek_emo_lvl2_to_lv1(limit: int = 10) -> List[EmoLvl2ToLv1]:
    """Retourne une liste de correspondances ordonnées par nom."""
    with get_session() as session:
        statement = select(EmoLvl2ToLv1).order_by(EmoLvl2ToLv1.emo_lvl2).limit(limit)
        return list(session.exec(statement))


def update_emo_lvl2_to_lv1(
    emo_lvl2: str, data: Dict
) -> Optional[EmoLvl2ToLv1]:
    """Met à jour les champs d'une correspondance existante."""
    with get_session() as session:
        mapping = session.get(EmoLvl2ToLv1, emo_lvl2)
        if not mapping:
            return None
        for key, value in data.items():
            setattr(mapping, key, value)
        session.add(mapping)
        session.commit()
        session.refresh(mapping)
        return mapping


def delete_emo_lvl2_to_lv1(emo_lvl2: str) -> bool:
    """Supprime une correspondance de la base."""
    with get_session() as session:
        mapping = session.get(EmoLvl2ToLv1, emo_lvl2)
        if not mapping:
            return False
        session.delete(mapping)
        session.commit()
        return True


# ----- CRUD pour les liens -----

def create_link(link: Link) -> Link:
    """Persiste un nouveau :class:`Link` dans la base."""
    with get_session() as session:
        session.add(link)
        session.commit()
        session.refresh(link)
        return link


def get_link(link_id: int) -> Optional[Link]:
    """Récupère un lien par son identifiant."""
    with get_session() as session:
        return session.get(Link, link_id)


def seek_links(limit: int = 10) -> List[Link]:
    """Retourne une liste de liens classés par id."""
    with get_session() as session:
        statement = select(Link).order_by(Link.link_id).limit(limit)
        return list(session.exec(statement))


def update_link(link_id: int, data: Dict) -> Optional[Link]:
    """Met à jour les champs d'un lien existant."""
    with get_session() as session:
        link = session.get(Link, link_id)
        if not link:
            return None
        for key, value in data.items():
            setattr(link, key, value)
        session.add(link)
        session.commit()
        session.refresh(link)
        return link


def delete_link(link_id: int) -> bool:
    """Supprime un lien de la base."""
    with get_session() as session:
        link = session.get(Link, link_id)
        if not link:
            return False
        session.delete(link)
        session.commit()
        return True


# ----- Gestion des associations lien-souvenir -----

def associate_link_souvenir(mem_id: int, link_id: int) -> LinkSouvenir:
    """Crée une association entre un souvenir et un lien."""
    with get_session() as session:
        association = LinkSouvenir(mem_id=mem_id, link_id=link_id)
        session.add(association)
        session.commit()
        session.refresh(association)
        return association


def delete_association_link_souvenir(mem_id: int, link_id: int) -> bool:
    """Supprime l'association entre un souvenir et un lien."""
    with get_session() as session:
        association = session.get(LinkSouvenir, (mem_id, link_id))
        if not association:
            return False
        session.delete(association)
        session.commit()
        return True


def get_links_pour_souvenir(mem_id: int) -> List[Link]:
    """Retourne tous les liens associés à un souvenir donné."""
    with get_session() as session:
        statement = (
            select(Link)
            .join(LinkSouvenir, Link.link_id == LinkSouvenir.link_id)
            .where(LinkSouvenir.mem_id == mem_id)
        )
        return list(session.exec(statement))
