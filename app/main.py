from fastapi import FastAPI
from app.dialogue.router import dialogue_router
from app.memory.db import init_db

init_db()

app = FastAPI(title="Arch.Noesis")

app.include_router(dialogue_router, prefix="/dialogue")

@app.get("/")
def read_root():
    return {"message": "Bienvenue dans Arch.Noesis 🖤"}
