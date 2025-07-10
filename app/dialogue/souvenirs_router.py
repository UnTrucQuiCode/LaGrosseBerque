from fastapi import APIRouter
from app.models import Souvenir
from app.memory.crud import creer_souvenir

router = APIRouter(prefix="/souvenirs", tags=["Souvenirs"])

@router.post("/", response_model=Souvenir)
def ajouter_souvenir(souvenir: Souvenir):
    """
    Enregistre un nouveau souvenir dans la base de données.
    """
    return creer_souvenir(souvenir)
