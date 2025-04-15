import os
import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipelines.socialstream_pipeline import socialstream_pipeline,upload_to_azure
from azure.storage.filedatalake import DataLakeServiceClient




# Default arguments for the DAG
default_args = {
    'owner': 'Atharv-Nanaware',
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
}

file_postfix = datetime.now().strftime("%Y%m%d")

dag = DAG(
    dag_id='etl_socialstream_pipeline',
    default_args=default_args,
    description='An ETL pipeline for extracting, processing, and uploading data to Azure Data Lake',
    schedule_interval='@daily',
    start_date=datetime(2025,1,1),
    catchup=False,
    tags=['social stream', 'etl', 'pipeline'],
)

# Task 1
extract_reddit_task = PythonOperator(
    task_id='extract_reddit_data',
    python_callable=socialstream_pipeline,
    op_kwargs={
        'file_name': f'socialstream_{file_postfix}',
        'subreddit': 'science+politics+technology+relationships',
        'time_filter': 'all',
        'limit': 5000
    },
    dag=dag,
)

# Task 2
upload_to_azure_task = PythonOperator(
    task_id='upload_to_azure',
    python_callable=upload_to_azure,
    op_kwargs={
        'file_name': f'socialstream_{file_postfix}.csv',
        'local_file_path': f'./data/socialstream_{file_postfix}.csv',
    },
    dag=dag,
)

# task dependencies
extract_reddit_task >> upload_to_azure_task
