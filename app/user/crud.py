"""CRUD operations for the user table."""

from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Tuple

from sqlalchemy import text
from sqlmodel import select

from app.models.user import User
from app.memory.db import get_session, init_db

DEFAULT_USERS: Tuple[Dict[str, object], ...] = (
    {"user_name": "Noesis", "permissions": "user", "type": "AI"},
    {"user_name": "Nemo", "permissions": "admin", "type": "human"},
)


def create_user(user: User) -> User:
    """Persist a new user in the database."""
    with get_session() as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def get_user(user_name: str) -> Optional[User]:
    """Retrieve a user by its identifier."""
    with get_session() as session:
        return session.get(User, user_name)


def list_users(limit: int = 100) -> List[User]:
    """Return users ordered by their identifier."""
    with get_session() as session:
        statement = select(User).order_by(User.user_name).limit(limit)
        return list(session.exec(statement))


def update_user(user_name: str, data: Dict[str, object]) -> Optional[User]:
    """Update mutable fields of a user."""
    mutable_fields = {"permissions", "type", "is_active"}
    with get_session() as session:
        user = session.get(User, user_name)
        if not user:
            return None
        for key, value in data.items():
            if key in mutable_fields:
                setattr(user, key, value)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def delete_user(user_name: str) -> bool:
    """Remove a user from the database."""
    with get_session() as session:
        user = session.get(User, user_name)
        if not user:
            return False
        session.delete(user)
        session.commit()
        return True


def ensure_default_users(defaults: Iterable[Dict[str, object]] = DEFAULT_USERS) -> None:
    """Insert default users when they are missing."""
    with get_session() as session:
        _ensure_user_schema(session)
        created = False
        for user_data in defaults:
            if session.get(User, user_data["user_name"]):
                continue
            session.add(User(**user_data))
            created = True
        if created:
            session.commit()


def _ensure_user_schema(session) -> None:
    """Guarantee that optional columns exist before interacting with data."""
    columns = {row[1] for row in session.exec(text("PRAGMA table_info('user')"))}
    if columns and "is_active" not in columns:
        session.exec(text('ALTER TABLE "user" ADD COLUMN is_active BOOLEAN DEFAULT 0'))
        session.commit()


# Ensure table exists and defaults are present when the module is imported.
init_db()
ensure_default_users()
