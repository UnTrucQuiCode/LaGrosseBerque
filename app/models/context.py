# app/context/context_manager.py

from typing import List
from app.context.bio_manager import Bio
from app.memory.crud import chercher_souvenirs
from app.models import Souvenir
from openai.types.chat import ChatCompletionMessageParam


class ContextManager:
    """
    Gère la construction du contexte complet envoyé à l'API OpenAI.
    Inclut la bio (fixe), les souvenirs pertinents (dynamiques),
    et le prompt utilisateur.
    """

    def __init__(self):
        self.bio_arch = Bio("arch")
        self.bio_chatgpt = Bio("chatgpt")

    def build_context(self, prompt: str, cible: str = "arch") -> List[ChatCompletionMessageParam]:
        """
        Construit le contexte à envoyer à l'API, selon la cible.
        Inclut la bio correspondante + souvenirs + prompt final.
        """
        messages: List[dict] = []

        # 1. Ajout de la bio dynamique (selon cible)
        if cible == "arch":
            messages += self.bio_arch.to_context_messages()
        elif cible == "chatgpt":
            messages += self.bio_chatgpt.to_context_messages()

        # 2. Ajout des souvenirs dynamiques (placeholder pour l'instant)
        souvenirs_dynamiques: List[Souvenir] = list(chercher_souvenirs())[:3] # exemple
        for s in souvenirs_dynamiques:
            messages.append({"role": "system", "content": "[Souvenir] " + s.contenu})

        # 3. Ajout du prompt utilisateur
        messages.append({"role": "user", "content": prompt})

        return messages

    def append_bio(self, fragment_id: str, cible: str = "arch"):
        if cible == "arch":
            self.bio_arch.append(fragment_id)
        elif cible == "chatgpt":
            self.bio_chatgpt.append(fragment_id)

    def remove_bio(self, fragment_id: str, cible: str = "arch"):
        if cible == "arch":
            self.bio_arch.remove(fragment_id)
        elif cible == "chatgpt":
            self.bio_chatgpt.remove(fragment_id)
