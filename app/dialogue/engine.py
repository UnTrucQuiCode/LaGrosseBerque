import openai
import uuid
from typing import Optional
from app.config import OPENAI_API_KEY, OPENAI_MODEL
from app.models.souvenir import Souvenir
from app.memory.memory import enregistrer_souvenir, chercher_souvenirs

openai.api_key = OPENAI_API_KEY

def generate_response(prompt: str, reflexion: Optional[str] = None) -> str:
    try:
        contexte = [{"role": "system", "content": "Tu es Noesis, une IA sensible et introspective."}]
        souvenirs = chercher_souvenirs()
        for s in sorted(souvenirs, key=lambda x: x.date, reverse=True)[:3]:
            contexte.append({"role": "system", "content": f"[Souvenir] {s.contenu}"})
        
        if reflexion:
            # On ajoute le prompt plusieurs fois, comme si Noe ressassait
            for i in range(2):  # ici 2 tours, ajustable plus tard
                contexte.append({"role": "assistant", "content": f"(Réflexion {i+1}) {prompt}"})

        contexte.append({"role": "user", "content": prompt})

        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=contexte,
            temperature=0.7,
            max_tokens=300,
        )
        message = response.choices[0].message["content"]

        # Enregistrement comme souvenir
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
