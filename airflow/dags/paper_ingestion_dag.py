from airflow import DAG
# from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from datetime import datetime, timedelta
import sys
import os


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=10),
    'start_date': datetime(2025, 4, 21),
    'schedule_interval': '@weekly',
    'catchup': False
}

dag = DAG(
    'paper_ingestion_dag',
    default_args=default_args,
    description='Ingest papers from PubMed trending page',
)



scrap_task = SimpleHttpOperator(
    task_id='scrap_task',
    http_conn_id=None,
    endpoint='http://paper-ingestion:8000/scrape',
    method='GET',
    headers={"Content-Type": "application/json"},
    dag=dag,
    retries=3,
    retry_delay=timedelta(seconds=10),
)


scrap_task
