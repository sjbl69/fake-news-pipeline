import pandas as pd
import os

def run_pipeline():
    print(" Lancement du pipeline...")

    # Fake data (simulation)
    data = [
        {
            "title": "News 1",
            "content": "Fake news content",
            "image_url": "http://image.com/1.jpg"
        },
        {
            "title": "News 2",
            "content": "Real news content",
            "image_url": "http://image.com/2.jpg"
        }
    ]

    df = pd.DataFrame(data)

    # Créer dossier si inexistant
    os.makedirs("data/processed", exist_ok=True)

    # Sauvegarde
    df.to_csv("data/processed/processed_news.csv", index=False)

    print(" Données sauvegardées dans data/processed/processed_news.csv")

if __name__ == "__main__":
    run_pipeline()