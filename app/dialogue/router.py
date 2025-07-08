from fastapi import APIRouter
from typing import Optional
from app.dialogue.engine import generate_response

dialogue_router = APIRouter()

@dialogue_router.post("/think") #sge si url /think avec une requete POST, fait :
def think(prompt: str, reflexion: Optional[str] = None):
    return {"response": generate_response(prompt, reflexion)}