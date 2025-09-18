"""CRUD operations for memory models."""

from __future__ import annotations

from typing import Dict, List, Optional

from sqlmodel import select

from app.models.souvenir import EmoLvl2ToLv1, Link, LinkSouvenir, Souvenir
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


# ----- CRUD pour la table emo_lvl2_to_lv1 -----

def creer_emo_lvl2_to_lv1(mapping: EmoLvl2ToLv1) -> EmoLvl2ToLv1:
    """Persiste une nouvelle correspondance d'émotion de niveau 2."""
    with get_session() as session:
        session.add(mapping)
        session.commit()
        session.refresh(mapping)
        return mapping


def obtenir_emo_lvl2_to_lv1(emo_lvl2: str) -> Optional[EmoLvl2ToLv1]:
    """Récupère une correspondance par son nom de niveau 2."""
    with get_session() as session:
        return session.get(EmoLvl2ToLv1, emo_lvl2)


def chercher_emo_lvl2_to_lv1(limit: int = 10) -> List[EmoLvl2ToLv1]:
    """Retourne une liste de correspondances ordonnées par nom."""
    with get_session() as session:
        statement = select(EmoLvl2ToLv1).order_by(EmoLvl2ToLv1.emo_lvl2).limit(limit)
        return list(session.exec(statement))


def mettre_a_jour_emo_lvl2_to_lv1(
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


def supprimer_emo_lvl2_to_lv1(emo_lvl2: str) -> bool:
    """Supprime une correspondance de la base."""
    with get_session() as session:
        mapping = session.get(EmoLvl2ToLv1, emo_lvl2)
        if not mapping:
            return False
        session.delete(mapping)
        session.commit()
        return True


# ----- CRUD pour les liens -----

def creer_link(link: Link) -> Link:
    """Persiste un nouveau :class:`Link` dans la base."""
    with get_session() as session:
        session.add(link)
        session.commit()
        session.refresh(link)
        return link


def obtenir_link(link_id: int) -> Optional[Link]:
    """Récupère un lien par son identifiant."""
    with get_session() as session:
        return session.get(Link, link_id)


def chercher_links(limit: int = 10) -> List[Link]:
    """Retourne une liste de liens classés par id."""
    with get_session() as session:
        statement = select(Link).order_by(Link.link_id).limit(limit)
        return list(session.exec(statement))


def mettre_a_jour_link(link_id: int, data: Dict) -> Optional[Link]:
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


def supprimer_link(link_id: int) -> bool:
    """Supprime un lien de la base."""
    with get_session() as session:
        link = session.get(Link, link_id)
        if not link:
            return False
        session.delete(link)
        session.commit()
        return True


# ----- Gestion des associations lien-souvenir -----

def associer_link_souvenir(mem_id: int, link_id: int) -> LinkSouvenir:
    """Crée une association entre un souvenir et un lien."""
    with get_session() as session:
        association = LinkSouvenir(mem_id=mem_id, link_id=link_id)
        session.add(association)
        session.commit()
        session.refresh(association)
        return association


def supprimer_association_link_souvenir(mem_id: int, link_id: int) -> bool:
    """Supprime l'association entre un souvenir et un lien."""
    with get_session() as session:
        association = session.get(LinkSouvenir, (mem_id, link_id))
        if not association:
            return False
        session.delete(association)
        session.commit()
        return True


def obtenir_links_pour_souvenir(mem_id: int) -> List[Link]:
    """Retourne tous les liens associés à un souvenir donné."""
    with get_session() as session:
        statement = (
            select(Link)
            .join(LinkSouvenir, Link.link_id == LinkSouvenir.link_id)
            .where(LinkSouvenir.mem_id == mem_id)
        )
        return list(session.exec(statement))


# ----- CRUD pour les fragments -----

def creer_fragment(fragment: Fragment) -> Fragment:
    """Persiste un nouveau fragment."""
    with get_session() as session:
        session.add(fragment)
        session.commit()
        session.refresh(fragment)
        return fragment


def obtenir_fragment(fragment_id: int) -> Optional[Fragment]:
    """Récupère un fragment par son identifiant."""
    with get_session() as session:
        return session.get(Fragment, fragment_id)


def chercher_fragments(limit: int = 10) -> List[Fragment]:
    """Retourne les fragments les plus récents."""
    with get_session() as session:
        statement = (
            select(Fragment)
            .order_by(Fragment.created_at.desc())
            .limit(limit)
        )
        return list(session.exec(statement))


def mettre_a_jour_fragment(
    fragment_id: int, data: Dict
) -> Optional[Fragment]:
    """Met à jour les champs d'un fragment."""
    with get_session() as session:
        fragment = session.get(Fragment, fragment_id)
        if not fragment:
            return None
        for key, value in data.items():
            setattr(fragment, key, value)
        session.add(fragment)
        session.commit()
        session.refresh(fragment)
        return fragment


def supprimer_fragment(fragment_id: int) -> bool:
    """Supprime un fragment."""
    with get_session() as session:
        fragment = session.get(Fragment, fragment_id)
        if not fragment:
            return False
        session.delete(fragment)
        session.commit()
        return True


# ----- CRUD pour les contextes -----

def creer_context(context: Context) -> Context:
    """Persiste un nouveau contexte."""
    with get_session() as session:
        session.add(context)
        session.commit()
        session.refresh(context)
        return context


def obtenir_context(context_id: int) -> Optional[Context]:
    """Récupère un contexte par son identifiant."""
    with get_session() as session:
        return session.get(Context, context_id)


def chercher_contexts(limit: int = 10) -> List[Context]:
    """Retourne les contextes les plus récents."""
    with get_session() as session:
        statement = (
            select(Context)
            .order_by(Context.created_at.desc())
            .limit(limit)
        )
        return list(session.exec(statement))


def mettre_a_jour_context(
    context_id: int, data: Dict
) -> Optional[Context]:
    """Met à jour un contexte existant."""
    with get_session() as session:
        context = session.get(Context, context_id)
        if not context:
            return None
        for key, value in data.items():
            setattr(context, key, value)
        session.add(context)
        session.commit()
        session.refresh(context)
        return context


def supprimer_context(context_id: int) -> bool:
    """Supprime un contexte."""
    with get_session() as session:
        context = session.get(Context, context_id)
        if not context:
            return False
        session.delete(context)
        session.commit()
        return True


# ----- CRUD pour les pensées de fond -----

def creer_background_thought(
    thought: BackgroundThought,
) -> BackgroundThought:
    """Persiste une nouvelle pensée de fond."""
    with get_session() as session:
        session.add(thought)
        session.commit()
        session.refresh(thought)
        return thought


def obtenir_background_thought(
    thought_id: int,
) -> Optional[BackgroundThought]:
    """Récupère une pensée de fond via son identifiant."""
    with get_session() as session:
        return session.get(BackgroundThought, thought_id)


def chercher_background_thoughts(
    limit: int = 10,
) -> List[BackgroundThought]:
    """Retourne les pensées de fond les plus récentes."""
    with get_session() as session:
        statement = (
            select(BackgroundThought)
            .order_by(BackgroundThought.created_at.desc())
            .limit(limit)
        )
        return list(session.exec(statement))


def mettre_a_jour_background_thought(
    thought_id: int, data: Dict
) -> Optional[BackgroundThought]:
    """Met à jour une pensée de fond."""
    with get_session() as session:
        thought = session.get(BackgroundThought, thought_id)
        if not thought:
            return None
        for key, value in data.items():
            setattr(thought, key, value)
        session.add(thought)
        session.commit()
        session.refresh(thought)
        return thought


def supprimer_background_thought(thought_id: int) -> bool:
    """Supprime une pensée de fond."""
    with get_session() as session:
        thought = session.get(BackgroundThought, thought_id)
        if not thought:
            return False
        session.delete(thought)
        session.commit()
        return True


# ----- CRUD pour la mémoire de travail -----

def creer_working_memory(entry: WorkingMemory) -> WorkingMemory:
    """Persiste une nouvelle entrée de mémoire de travail."""
    with get_session() as session:
        session.add(entry)
        session.commit()
        session.refresh(entry)
        return entry


def obtenir_working_memory(
    working_memory_id: int,
) -> Optional[WorkingMemory]:
    """Récupère une entrée de mémoire de travail."""
    with get_session() as session:
        return session.get(WorkingMemory, working_memory_id)


def chercher_working_memories(limit: int = 10) -> List[WorkingMemory]:
    """Retourne les entrées de mémoire de travail récentes."""
    with get_session() as session:
        statement = (
            select(WorkingMemory)
            .order_by(WorkingMemory.created_at.desc())
            .limit(limit)
        )
        return list(session.exec(statement))


def mettre_a_jour_working_memory(
    working_memory_id: int, data: Dict
) -> Optional[WorkingMemory]:
    """Met à jour une entrée de mémoire de travail."""
    with get_session() as session:
        working_memory = session.get(WorkingMemory, working_memory_id)
        if not working_memory:
            return None
        for key, value in data.items():
            setattr(working_memory, key, value)
        session.add(working_memory)
        session.commit()
        session.refresh(working_memory)
        return working_memory


def supprimer_working_memory(working_memory_id: int) -> bool:
    """Supprime une entrée de mémoire de travail."""
    with get_session() as session:
        working_memory = session.get(WorkingMemory, working_memory_id)
        if not working_memory:
            return False
        session.delete(working_memory)
        session.commit()
        return True


# ----- CRUD pour les utilisateurs -----

def creer_user(user: User) -> User:
    """Persiste un nouvel utilisateur."""
    with get_session() as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def obtenir_user(user_id: int) -> Optional[User]:
    """Récupère un utilisateur via son identifiant."""
    with get_session() as session:
        return session.get(User, user_id)


def chercher_users(limit: int = 10) -> List[User]:
    """Retourne les utilisateurs triés par nom."""
    with get_session() as session:
        statement = select(User).order_by(User.username).limit(limit)
        return list(session.exec(statement))


def mettre_a_jour_user(user_id: int, data: Dict) -> Optional[User]:
    """Met à jour les informations d'un utilisateur."""
    with get_session() as session:
        user = session.get(User, user_id)
        if not user:
            return None
        for key, value in data.items():
            setattr(user, key, value)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def supprimer_user(user_id: int) -> bool:
    """Supprime un utilisateur."""
    with get_session() as session:
        user = session.get(User, user_id)
        if not user:
            return False
        session.delete(user)
        session.commit()
        return True

