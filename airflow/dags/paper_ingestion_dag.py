from airflow import DAG
# from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from datetime import datetime, timedelta
import sys
import os

# sys.path.append(os.path.join(os.path.dirname(__file__), '../../paper_ingestion'))
# sys.path.append('/opt/airflow/paper_ingestion')


# from historical_scrapper import scrape_articles


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'start_date': datetime(2025, 4, 5),
    'schedule_interval': '@daily',
    'catchup': False
}

dag = DAG(
    'paper_ingestion_dag',
    default_args=default_args,
    description='Ingest papers from PubMed trending page',
)


# def run_scrapper():
#     scrape_articles()


# scrap_task = PythonOperator(
#     task_id='scrap_task',
#     python_callable=scrape_articles,
#     dag=dag,
# )

scrap_task = SimpleHttpOperator(
    task_id='scrap_task',
    # http_conn_id='scrapper_api',  # You'll define this in Airflow connections
    endpoint='http://paper-ingestion:8000/scrape',
    method='GET',
    http_conn_id=None,
    dag=dag,
)


scrap_task
