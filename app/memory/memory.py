from typing import List, Optional
from app.models.souvenir import Souvenir

souvenirs: List[Souvenir] = []

def enregistrer_souvenir(souvenir: Souvenir):
    souvenirs.append(souvenir)

def chercher_souvenirs(contexte: Optional[str] = None) -> List[Souvenir]:
    if contexte:
        return [s for s in souvenirs if contexte in (s.contexte or "")]
    return souvenirs