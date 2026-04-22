import requests
import os
import json
import uuid
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")

if not API_KEY:
    raise ValueError("NEWS_API_KEY manquante dans le fichier .env")

URL = "https://newsapi.org/v2/top-headlines"


def fetch_news():
    params = {
        "apiKey": API_KEY,
        "country": "us",
        "pageSize": 10
    }

    try:
        response = requests.get(URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Erreur requête :", e)
        return []

    data = response.json()

    if data.get("status") != "ok":
        print("Erreur API :", data)
        return []

    articles = data.get("articles", [])
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

        if all([
            cleaned["title"],
            cleaned["text"],
            cleaned["image_url"]
        ]):
            cleaned_articles.append(cleaned)

    return cleaned_articles


def save_to_json(data):
    os.makedirs("data", exist_ok=True)

    filename = f"data/news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    news = fetch_news()
    save_to_json(news)

    print(f"{len(news)} articles sauvegardés")