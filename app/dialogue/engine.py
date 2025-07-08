import openai
import uuid
from typing import Optional
from app.config import OPENAI_API_KEY, OPENAI_MODEL
from app.models.souvenir import Souvenir
from app.memory.memory import enregistrer_souvenir, chercher_souvenirs
from app.memory.context import ContextManager

openai.api_key = OPENAI_API_KEY

def generate_response(prompt: str, reflexion: Optional[str] = None) -> str:
    try:
        context_manager = ContextManager()
        messages = context_manager.construire_contexte(prompt)

        if reflexion:
            for i in range(2):
                messages.insert(-1, {"role": "assistant", "content": f"(Réflexion {i+1}) {prompt}"})

        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=300,
        )

        message = response.choices[0].message["content"]

        # Enregistrement du souvenir (inchangé)
        souvenir = Souvenir(
            id=str(uuid.uuid4()),
            auteur="Nemo",
            contenu=f"{prompt}\n→ {message}",
            contexte="dialogue"
        )
        enregistrer_souvenir(souvenir)

        return message

    except Exception as e:
        return f"Erreur : {str(e)}"

