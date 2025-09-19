# app/context/bio_manager.py

from typing import List, TYPE_CHECKING

from app.memory.crud import chercher_souvenirs

if TYPE_CHECKING:
    from app.models.memory import Souvenir

class Bio:
    """
    Gère dynamiquement une "bio" composée de fragments mémoriels.
    Chaque fragment est référencé par son `id` (UUID) ou toute clé unique dans la mémoire.
    """

    def __init__(self, target: str):
        """
        Initialise une bio pour une cible donnée : "arch" ou "chatgpt".
        Chaque instance conserve sa propre liste de fragments.
        """
        self.target = target
        # Identifiants des souvenirs conservés dans la bio
        self.bio_fragments: List[int] = []

    def append(self, fragment_id: int):
        """
        Ajoute un fragment à la bio s'il n'y est pas déjà.
        """
        if fragment_id not in self.bio_fragments:
            self.bio_fragments.append(fragment_id)

    def remove(self, fragment_id: int):
        """
        Supprime un fragment de la bio s'il est présent.
        """
        if fragment_id in self.bio_fragments:
            self.bio_fragments.remove(fragment_id)

    def get_fragments(self) -> List["Souvenir"]:
        """
        Retourne les souvenirs correspondants aux IDs de la bio,
        dans l'ordre d'insertion.
        """
        all_souvenirs = {s.mem_id: s for s in chercher_souvenirs()}  # index par ID
        return [
            all_souvenirs[sid]
            for sid in self.bio_fragments
            if sid in all_souvenirs
        ]

    def to_context_messages(self) -> List[dict]:
        """
        Transforme les fragments de bio en messages formatés pour l'API OpenAI.
        Par exemple, pour Arch : prefixés par [Bio-arch], pour ChatGPT : [Bio-chatgpt].
        """
        messages: List[dict] = []
        prefix = f"[Bio-{self.target}] "

        for souvenir in self.get_fragments():
            content = prefix + souvenir.content
            messages.append({"role": "system", "content": content})

        return messages

# Exemple d'utilisation (à inclure dans ContextManager ou ailleurs) :
# bio_arch = Bio("arch")
# bio_arch.append("uuid-de-fragment")
# ... puis, au moment de build de contexte :
# messages = bio_arch.to_context_messages() + other_messages
