import sys
import os
from datetime import datetime

# ajouter mon projet au path
sys.path.append('/mnt/c/Users/selma/Desktop/fake-news-pipeline')

from airflow import DAG
from airflow.operators.python import PythonOperator

# imports de TON projet
from src.extract.news_api import fetch_news
from src.transform.pipeline import transform_data


# FONCTIONS

def extract():
    data = fetch_news()
    print(f"{len(data)} articles récupérés")
    return data


def transform(**context):
    ti = context['ti']
    data = ti.xcom_pull(task_ids='extract')

    if not data:
        print("Aucune donnée à transformer")
        return []

    transformed = transform_data(data)
    print(f"{len(transformed)} articles transformés")
    return transformed


def load(**context):
    ti = context['ti']
    data = ti.xcom_pull(task_ids='transform')

    if not data:
        print("Aucune donnée à charger")
        return

    print("Chargement simulé OK")


#  DAG

with DAG(
    dag_id="etl_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    task_extract = PythonOperator(
        task_id="extract",
        python_callable=extract
    )

    task_transform = PythonOperator(
        task_id="transform",
        python_callable=transform,
        provide_context=True
    )

    task_load = PythonOperator(
        task_id="load",
        python_callable=load,
        provide_context=True
    )

    # pipeline
    task_extract >> task_transform >> task_load