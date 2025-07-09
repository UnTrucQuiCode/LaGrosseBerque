
def create_msg(role: str, content: str) -> dict:
    """
    Crée un message structuré pour l'API OpenAI.
    Paramètres :
        - role : "system", "user" ou "assistant"
        - content : contenu textuel du message
    Retour :
        - dict représentant un message conforme au format OpenAI
    """
    return {"role": role, "content": content}
