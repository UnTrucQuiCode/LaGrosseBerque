from fastapi import FastAPI
from app.memory.db import init_db
from app.dialogue.router import dialogue_router
from app.dialogue.souvenirs_router import router as souvenirs_router

if __name__ == "__main__":
    init_db()

app = FastAPI(title="Arch.Noesis")

app.include_router(souvenirs_router)
app.include_router(dialogue_router, prefix="/dialogue")

@app.get("/")
def read_root():
    return {"message": "Bienvenue dans Arch.Noesis 🖤"}
