from fastapi import APIRouter
from app.models.memory import Souvenir
from app.memory.crud import create_souvenir

router = APIRouter(prefix="/souvenirs", tags=["Souvenirs"])

@router.post("/", response_model=Souvenir)
def ajouter_souvenir(souvenir: Souvenir):
    """
    Enregistre un nouveau souvenir dans la base de données.
    """
    return create_souvenir(souvenir)
