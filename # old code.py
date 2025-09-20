# old code bio manager

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

#--------------
# old code context model

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
        souvenirs_dynamiques: List[Souvenir] = list(chercher_souvenirs())[:3]  # exemple
        for s in souvenirs_dynamiques:
            messages.append({"role": "system", "content": "[Souvenir] " + s.content})

        # 3. Ajout du prompt utilisateur
        messages.append({"role": "user", "content": prompt})

        return messages

    def append_bio(self, fragment_id: int, cible: str = "arch"):
        if cible == "arch":
            self.bio_arch.append(fragment_id)
        elif cible == "chatgpt":
            self.bio_chatgpt.append(fragment_id)

    def remove_bio(self, fragment_id: int, cible: str = "arch"):
        if cible == "arch":
            self.bio_arch.remove(fragment_id)
        elif cible == "chatgpt":
            self.bio_chatgpt.remove(fragment_id)
