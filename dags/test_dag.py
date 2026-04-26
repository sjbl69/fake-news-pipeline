from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def hello():
    print("Hello Airflow")

with DAG(
    dag_id="test_simple",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    t1 = PythonOperator(
        task_id="hello_task",
        python_callable=hello
    )