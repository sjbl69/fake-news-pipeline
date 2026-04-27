from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import pandas as pd

# PATHS PORTABLES
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
TRANSFORMED_DIR = os.path.join(DATA_DIR, "transformed")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

# ETAPES PIPELINE

def extract():
    print(" Extraction des données...")

    data = [
        {"title": "News 1", "content": "Fake news content", "image_url": "http://image.com/1.jpg"},
        {"title": "News 2", "content": "Real news content", "image_url": "http://image.com/2.jpg"},
    ]

    os.makedirs(RAW_DIR, exist_ok=True)

    raw_path = os.path.join(RAW_DIR, "raw_news.csv")
    pd.DataFrame(data).to_csv(raw_path, index=False)

    print(f" Données extraites -> {raw_path}")


def transform():
    print(" Transformation des données...")

    raw_path = os.path.join(RAW_DIR, "raw_news.csv")

    if not os.path.exists(raw_path):
        raise FileNotFoundError(" Fichier raw introuvable")

    df = pd.read_csv(raw_path)

    # Nettoyage simple
    df = df.dropna()

    os.makedirs(TRANSFORMED_DIR, exist_ok=True)

    transformed_path = os.path.join(TRANSFORMED_DIR, "transformed_news.csv")
    df.to_csv(transformed_path, index=False)

    print(f" Données transformées -> {transformed_path}")


def load():
    print(" Chargement des données...")

    transformed_path = os.path.join(TRANSFORMED_DIR, "transformed_news.csv")

    if not os.path.exists(transformed_path):
        raise FileNotFoundError(" Fichier transformé introuvable")

    df = pd.read_csv(transformed_path)

    os.makedirs(PROCESSED_DIR, exist_ok=True)

    output_path = os.path.join(PROCESSED_DIR, "processed_news.csv")
    df.to_csv(output_path, index=False)

    print(f" Données sauvegardées -> {output_path}")


# DAG CONFIG

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
}

with DAG(
    dag_id="fake_news_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
    description="ETL pipeline for fake news detection",
) as dag:

    extract_task = PythonOperator(
        task_id="extract_task",
        python_callable=extract,
    )

    transform_task = PythonOperator(
        task_id="transform_task",
        python_callable=transform,
    )

    load_task = PythonOperator(
        task_id="load_task",
        python_callable=load,
    )

    extract_task >> transform_task >> load_task