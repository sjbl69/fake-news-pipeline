import os
from dotenv import load_dotenv

def get_env_variable(var_name: str) -> str:
    """
    Récupère une variable d'environnement et vérifie qu'elle existe.

    Args:
        var_name (str): Nom de la variable d'environnement à récupérer.

    Returns:
        str: Valeur de la variable d'environnement.

    Raises:
        ValueError: Si la variable d'environnement n'est pas définie.
    """
    value = os.getenv(var_name)
    if value is None:
        raise ValueError(f"La variable d'environnement '{var_name}' est manquante")
    return value

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupération sécurisée de la clé API News
NEWS_API_KEY = get_env_variable("NEWS_API_KEY")