import os
import logging
import requests

logging.basicConfig(level=logging.INFO)


def download_image(url, save_path):
    """
    Télécharge une image et retourne True si succès
    """
    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            return True
        else:
            logging.warning(f"Image non téléchargée : {url}")
            return False

    except Exception as e:
        logging.error(f"Erreur téléchargement image : {e}")
        return False


def download_images(data, folder="data/raw/images"):
    """
    Télécharge toutes les images et met à jour image_path uniquement si succès
    """
    os.makedirs(folder, exist_ok=True)

    for article in data:
        if article["image_url"]:
            filename = os.path.join(folder, f"{article['id']}.jpg")

            success = download_image(article["image_url"], filename)

            #  MAJ UNIQUEMENT SI SUCCÈS
            if success:
                article["image_path"] = filename