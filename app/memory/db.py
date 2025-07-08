from typing import Optional
from sqlmodel import SQLModel, create_engine, Session, select
from app.models.souvenir import Souvenir

sqlite_file = "souvenirs.db"
engine = create_engine(f"sqlite:///{sqlite_file}", echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)

def enregistrer_souvenir(souvenir: Souvenir):
    with Session(engine) as session:
        session.add(souvenir)
        session.commit()

def chercher_souvenirs(contexte: Optional[str] = None):
    with Session(engine) as session:
        if contexte:
            query = select(Souvenir).where(Souvenir.contexte == contexte)
        else:
            query = select(Souvenir)
        results = session.exec(query)
        return results.all()
