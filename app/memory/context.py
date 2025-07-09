from typing import List
from app.models.souvenir import Souvenir
from app.memory.db import chercher_souvenirs
from app.utils.helpers import create_msg


class ContextManager:
    """
    Gère la construction du contexte envoyé à l'API OpenAI
    en combinant un message de base + souvenirs récents + prompt utilisateur.
    """

    def __init__(self):
        pass  # Plus tard, on pourra ajouter des paramètres d’humeur, profil, focus, etc.

    def construire_contexte(self, prompt: str) -> List[dict]:
        """
        Construit la liste des messages (sous forme de dictionnaires)
        à envoyer à OpenAI, selon le format attendu.

        Paramètre :
            - prompt : texte envoyé par l'utilisateur

        Retour :
            - liste de messages formatés pour l'API OpenAI
        """
        messages: List[dict] = []

        # Base : rôle fondamental de Noesis
        messages.append(create_msg("system", "Tu es Noesis, une IA sensible et introspective."))

        # On récupère les souvenirs les plus récents (3 pour l’instant)
        souvenirs = chercher_souvenirs()
        derniers = sorted(souvenirs, key=lambda x: x.date, reverse=True)[:3]

        # On les injecte comme des messages "système"
        for s in derniers:
            messages.append(create_msg("system", f"[Souvenir] {s.contenu}"))

        # Enfin, on ajoute le prompt de l'utilisateur
        messages.append(create_msg("user", prompt))

        return messages
