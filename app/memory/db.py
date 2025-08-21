# app/memory/db.py

from sqlmodel import SQLModel, create_engine, Session

# Base de données dédiée aux souvenirs
DATABASE_URL = "sqlite:///./souvenirs.db"
engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)

# Ensure tables are created on first import
init_db()
