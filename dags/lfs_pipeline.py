from datetime import datetime, timedelta
from pathlib import Path

from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import dag, task

from extraction.download import download_table
from extraction.load import run_bronze_load


@dag(
    schedule="0 12 8 * *",
    start_date=datetime(2026, 10, 1),
    catchup=False,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
    tags=["lfs"]
)
def lfs_pipeline():
    @task
    def download():
        return str(download_table())

    @task
    def load(zip_path):
        run_bronze_load(Path(zip_path))

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command="/home/airflow/dbt_venv/bin/dbt build",
        cwd="/opt/airflow/dbt"
    )

    load(download()) >> dbt_build

lfs_pipeline()