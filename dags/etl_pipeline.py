from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import logging
import json
import os
import sys

# FIX PATH PROJET
PROJECT_PATH = "/home/selma/airflow"

if PROJECT_PATH not in sys.path:
    sys.path.insert(0, PROJECT_PATH)

# IMPORTS PROJET

from src.extract.news_api import fetch_news
from src.transform.pipeline import transform_data

# PATHS FICHIERS
RAW_PATH = os.path.join(PROJECT_PATH, "data/raw/raw_data.json")
PROCESSED_PATH = os.path.join(PROJECT_PATH, "data/processed/clean_data.json")
FINAL_PATH = os.path.join(PROJECT_PATH, "data/final/final_data.json")

# TASK 1 : EXTRACTION
def extract_task():
    logging.info(" Extraction des données...")

    data = fetch_news()

    if not data:
        raise ValueError(" Aucune donnée extraite")

    os.makedirs(os.path.dirname(RAW_PATH), exist_ok=True)

    with open(RAW_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    logging.info(" Données extraites et sauvegardées")

# TASK 2 : TRANSFORMATION
def transform_task():
    logging.info(" Transformation des données...")

    if not os.path.exists(RAW_PATH):
        raise FileNotFoundError(" Fichier raw introuvable")

    with open(RAW_PATH, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    clean_data = transform_data(raw_data)

    os.makedirs(os.path.dirname(PROCESSED_PATH), exist_ok=True)

    with open(PROCESSED_PATH, "w", encoding="utf-8") as f:
        json.dump(clean_data, f, indent=2, ensure_ascii=False)

    logging.info(" Données transformées")

# TASK 3 : LOAD
def load_task():
    logging.info(" Chargement des données...")

    if not os.path.exists(PROCESSED_PATH):
        raise FileNotFoundError(" Données transformées introuvables")

    with open(PROCESSED_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    os.makedirs(os.path.dirname(FINAL_PATH), exist_ok=True)

    with open(FINAL_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    logging.info(" Données chargées avec succès")

# DAG CONFIG
default_args = {
    "owner": "selma",
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
}

with DAG(
    dag_id="etl_multimodal_pipeline",
    default_args=default_args,
    schedule=None,   
    catchup=False,
    description="Pipeline ETL multimodal",
) as dag:

    extract = PythonOperator(
        task_id="extract_data",
        python_callable=extract_task
    )

    transform = PythonOperator(
        task_id="transform_data",
        python_callable=transform_task
    )

    load = PythonOperator(
        task_id="load_data",
        python_callable=load_task
    )

    extract >> transform >> load