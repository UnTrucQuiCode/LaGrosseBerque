import uuid
from openai import OpenAI
from app.config import OPENAI_API_KEY, OPENAI_MODEL
from app.models import ContextManager
from app.models import Souvenir
from app.memory.crud import enregistrer_souvenir
from typing import Optional
from app.utils.logger import logger  # Import du logger

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_response(prompt: str, reflexion: Optional[str] = None) -> str:
    try:
        context_manager = ContextManager()
        context_manager.append_bio("3df2-98f3-bio-id", cible="arch")

        messages = context_manager.build_context(prompt="Parle-moi de la mémoire")

        if reflexion:
            for i in range(2):
                messages.insert(-1, {"role": "assistant", "content": f"(Réflexion {i+1}) {prompt}"})

        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=300,
        )

        message = response.choices[0].message.content
        if message is None:
            return "Erreur : réponse vide du modèle"

        souvenir = Souvenir(
            id=str(uuid.uuid4()),
            auteur="Nemo",
            contenu=f"{prompt}\n→ {message}",
            contexte="dialogue"
        )
        enregistrer_souvenir(souvenir)

        return message

    except Exception as e:
        logger.error(f"Erreur lors de la génération de réponse : {e}")  # Enregistre dans le fichier log
        return f"Erreur : {str(e)}"
