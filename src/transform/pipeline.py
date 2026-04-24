import json
import logging
from pathlib import Path

from src.transform.cleaning import clean_text
from src.transform.validation import is_valid_article
from src.transform.utils import normalize_date

logging.basicConfig(level=logging.INFO)

RAW_PATH = Path("data/raw/articles.json")
PROCESSED_PATH = Path("data/processed/clean_articles.json")


def load_data():
    logging.info(" Chargement des données brutes...")
    with open(RAW_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def transform_data(raw_articles):
    logging.info(" Transformation des données...")

    clean_articles = []

    for article in raw_articles:

        if not is_valid_article(article):
            logging.warning(" Article invalide ignoré")
            continue

        clean_article = {
            "title": clean_text(article.get("title")),
            "content": clean_text(article.get("description")),
            "image_url": article.get("urlToImage"),
            "source": article.get("source", {}).get("name"),
            "published_at": normalize_date(article.get("publishedAt")),
            "url": article.get("url"),
        }

        clean_articles.append(clean_article)

    logging.info(f" {len(clean_articles)} articles transformés")
    return clean_articles


def save_data(data):
    logging.info(" Sauvegarde des données transformées...")

    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(PROCESSED_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def run_pipeline():
    raw_data = load_data()

    if not raw_data:
        logging.error(" Aucune donnée trouvée")
        return

    processed_data = transform_data(raw_data)
    save_data(processed_data)


if __name__ == "__main__":
    run_pipeline()