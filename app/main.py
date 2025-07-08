from fastapi import FastAPI
from app.dialogue.router import dialogue_router

app = FastAPI(title="Arch.Noesis")

app.include_router(dialogue_router, prefix="/dialogue")

@app.get("/")
def read_root():
    return {"message": "Bienvenue dans Arch.Noesis 🖤"}
