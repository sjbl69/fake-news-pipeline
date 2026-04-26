from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import logging
import json
import os
import sys

# FIX PATH (IMPORTANT)
PROJECT_PATH = "/home/selma/airflow"

if PROJECT_PATH not in sys.path:
    sys.path.insert(0, PROJECT_PATH)

# IMPORTS
from src.extract.news_api import fetch_news
from src.transform.pipeline import transform_data

# PATHS
RAW_PATH = os.path.join(PROJECT_PATH, "data/raw/raw_data.json")
PROCESSED_PATH = os.path.join(PROJECT_PATH, "data/processed/clean_data.json")
FINAL_PATH = os.path.join(PROJECT_PATH, "data/final/final_data.json")

# TASKS
def extract_task():
    logging.info("Extraction...")

    data = fetch_news()

    if not data:
        raise ValueError("Aucune donnée")

    os.makedirs(os.path.dirname(RAW_PATH), exist_ok=True)

    with open(RAW_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def transform_task():
    logging.info("Transformation...")

    with open(RAW_PATH, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    clean_data = transform_data(raw_data)

    os.makedirs(os.path.dirname(PROCESSED_PATH), exist_ok=True)

    with open(PROCESSED_PATH, "w", encoding="utf-8") as f:
        json.dump(clean_data, f, indent=2, ensure_ascii=False)


def load_task():
    logging.info("Loading...")

    with open(PROCESSED_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    os.makedirs(os.path.dirname(FINAL_PATH), exist_ok=True)

    with open(FINAL_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# DAG
default_args = {
    "owner": "selma",
    "start_date": datetime(2024, 1, 1),
}

with DAG(
    dag_id="etl_multimodal_pipeline",
    default_args=default_args,
    schedule=None,   
    catchup=False,
) as dag:

    extract = PythonOperator(
        task_id="extract",
        python_callable=extract_task
    )

    transform = PythonOperator(
        task_id="transform",
        python_callable=transform_task
    )

    load = PythonOperator(
        task_id="load",
        python_callable=load_task
    )

    extract >> transform >> load