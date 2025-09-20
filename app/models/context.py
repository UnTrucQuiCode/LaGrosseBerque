# app/context/context_manager.py

from typing import List
# from app.context.bio_manager import Bio
from app.memory.crud import seek_souvenirs
from .memory import Souvenir
from openai.types.chat import ChatCompletionMessageParam

class ContextManager:
    """
    Gère la construction du contexte complet envoyé à l'API OpenAI.
    Inclut la bio (fixe), les souvenirs pertinents (dynamiques),
    et le prompt utilisateur.
    """


