# app/memory/db.py

from sqlmodel import SQLModel, create_engine, Session
from app.memory.models import Souvenir

DATABASE_URL = "sqlite:///./arch.db"
engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)
