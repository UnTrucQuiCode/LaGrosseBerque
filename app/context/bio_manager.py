# app/context/bio_manager.py

from typing import List, TYPE_CHECKING

from app.memory.crud import seek_souvenirs

if TYPE_CHECKING:
    from app.models.memory import Souvenir


# Exemple d'utilisation (à inclure dans ContextManager ou ailleurs) :
# bio_arch = Bio("arch")
# bio_arch.append("uuid-de-fragment")
# ... puis, au moment de build de contexte :
# messages = bio_arch.to_context_messages() + other_messages
