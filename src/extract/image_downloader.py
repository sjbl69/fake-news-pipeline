import os
import requests


def download_image(url, save_path):
    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
        else:
            print(f" Image non téléchargée : {url}")

    except Exception as e:
        print(f" Erreur téléchargement image : {e}")


def download_images(data, folder="data/raw/images"):
    os.makedirs(folder, exist_ok=True)

    for article in data:
        if article["image_url"]:
            filename = os.path.join(folder, f"{article['id']}.jpg")

            download_image(article["image_url"], filename)

            # Mettre à jour le chemin local
            article["image_path"] = filename