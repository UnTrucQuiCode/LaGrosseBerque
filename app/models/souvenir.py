from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Souvenir(BaseModel): #sge Majuscule pour différentier les classes des fonctions
    id: str
    auteur: str
    contenu: str
    contexte: Optional[str] = None
    date: datetime = datetime.now()
    importance_globale: float = 0.5
