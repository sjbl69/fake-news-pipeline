import os
import json
import uuid
import logging
import requests
import sys
from datetime import datetime, timezone
from dotenv import load_dotenv

from src.extract.utils import is_valid_image
from src.extract.image_downloader import download_images

# Logs
logging.basicConfig(level=logging.INFO)

# Charger variables d'environnement
load_dotenv()

URL = "https://newsapi.org/v2/top-headlines"


def fetch_news(country="us", page_size=10, max_pages=3):
    """
    Extraction brute depuis l'API avec pagination
    """
    api_key = os.getenv("NEWS_API_KEY")

    if not api_key:
      logging.error(" NEWS_API_KEY manquante dans le fichier .env")
    sys.exit(1)


    all_articles = []

    for page in range(1, max_pages + 1):
        params = {
            "apiKey": api_key,
            "country": country,
            "pageSize": page_size,
            "page": page
        }

        try:
            response = requests.get(URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("status") != "ok":
                logging.error(f"Erreur API : {data}")
                continue

            articles = data.get("articles", [])

            if not articles:
                break

            all_articles.extend(articles)

        except requests.exceptions.RequestException as e:
            logging.error(f"Erreur requête : {e}")

    return all_articles


def parse_articles(articles):
    """
    Nettoyage + structuration
    """
    cleaned_articles = []

    for article in articles:
        cleaned = {
            "id": str(uuid.uuid4()),
            "title": article.get("title"),
            "text": article.get("description"),
            "article_url": article.get("url"),
            "image_url": article.get("urlToImage"),
            "image_path": None,
            "source_name": article.get("source", {}).get("name"),
            "language": "en",
            "published_at": article.get("publishedAt"),
            "collected_at": datetime.now(timezone.utc).isoformat(),
            "label": None,
            "raw_source": "news_api"
        }

        #  Filtrer contenu exploitable + image valide
        if all([
            cleaned["title"],
            cleaned["text"],
            cleaned["image_url"]
        ]) and is_valid_image(cleaned["image_url"]):
            cleaned_articles.append(cleaned)

    return cleaned_articles


def save_to_json(data):
    """
    Sauvegarde JSON
    """
    os.makedirs("data/raw", exist_ok=True)

    filename = f"data/raw/news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    logging.info(f"Données sauvegardées : {filename}")


def main():
    logging.info(" Début extraction...")

    raw_articles = fetch_news()

    def main():
     logging.info(" Début extraction...")

    raw_articles = fetch_news()

    if not raw_articles:
        logging.error(" Aucune donnée récupérée. Arrêt du script.")
        return

    cleaned_articles = parse_articles(raw_articles)

    # Télécharger images
    download_images(cleaned_articles)

    save_to_json(cleaned_articles)

    logging.info(f" {len(cleaned_articles)} articles prêts")
    cleaned_articles = parse_articles(raw_articles)

    #  Télécharger images 
    download_images(cleaned_articles)

    save_to_json(cleaned_articles)

    logging.info(f" {len(cleaned_articles)} articles prêts")


if __name__ == "__main__":
    main()