import logging
import os

# Créer un dossier "logs" s’il n’existe pas
if not os.path.exists("logs"):
    os.makedirs("logs")

# Créer un logger nommé "arch"
logger = logging.getLogger("arch")
logger.setLevel(logging.INFO)  # Peut être DEBUG, INFO, WARNING, ERROR, CRITICAL

# Créer un gestionnaire de fichier qui enregistre les erreurs dans logs/errors.log
file_handler = logging.FileHandler("logs/errors.log")
file_handler.setLevel(logging.ERROR)  # On n'enregistre que les erreurs

# Définir le format du log (date, niveau, message)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
file_handler.setFormatter(formatter)

# Ajouter ce handler au logger principal
logger.addHandler(file_handler)
