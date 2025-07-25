from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'lapes_olist_pipeline',
    default_args=default_args,
    description='Pipeline ELT para o dataset Olist (Bronze → Silver)',
    schedule_interval='0 6 * * *',  # diário às 06:00
    start_date=datetime(2025, 7, 26),
    catchup=False,
    tags=['lapes', 'elt', 'olist'],
) as dag:

    # 1) Baixar e extrair o dataset
    download_task = BashOperator(
        task_id='download_olist',
        bash_command='python -m src.elt.01_download_olist',
    )

    # 2) Converter CSV → Parquet
    csv_to_parquet_task = BashOperator(
        task_id='csv_to_parquet',
        bash_command='python -m src.elt.02_csv_to_parquet',
    )

    # 3) Carregar Bronze e Silver (truncate + load + copy)
    load_bronze_silver_task = BashOperator(
        task_id='load_bronze_silver',
        bash_command='python -m src.elt.03_load_bronze_to_db',
    )

    # Definição de ordem
    download_task >> csv_to_parquet_task >> load_bronze_silver_task
