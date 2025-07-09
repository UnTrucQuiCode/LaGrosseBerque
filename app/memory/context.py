from app.memory.memory import chercher_souvenirs
from app.models.souvenir import Souvenir
from typing import List, Dict

class ContextManager:
    def __init__(self):
        pass  # plus tard, on pourra passer des paramètres (humeur, thème, etc.)

    def construire_contexte(self, prompt: str) -> list[ChatCompletionMessageParam]:
        messages: list[ChatCompletionMessageParam] = []
    
        messages.append({"role": "system", "content": "Tu es Noesis, une IA sensible et introspective."})

        souvenirs = chercher_souvenirs()
        derniers = sorted(souvenirs, key=lambda x: x.date, reverse=True)[:3]

        for s in derniers:
            messages.append({"role": "system", "content": f"[Souvenir] {s.contenu}"})

        messages.append({"role": "user", "content": prompt})

        return messages
