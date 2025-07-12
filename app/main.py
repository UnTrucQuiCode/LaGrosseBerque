from fastapi import FastAPI
from app.memory.db import init_db
from app.dialogue.router import dialogue_router
from app.dialogue.souvenirs_router import router as souvenirs_router
from sqlmodel import SQLModel
from app.memory.db import engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Arch.Noesis")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
if __name__ == "__main__":
    init_db()
"""

def init_db():
    SQLModel.metadata.create_all(engine) # cree la db

@app.on_event("startup") # demarre la db a l'event startup
def on_startup():
    init_db()


app.include_router(souvenirs_router)
app.include_router(dialogue_router, prefix="/dialogue")

@app.get("/")
def read_root():
    return {"message": "Bienvenue dans Arch.Noesis 🖤"}
