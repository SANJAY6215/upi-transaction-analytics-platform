from airflow import DAG
from airflow.operators.bash import BashOperator  # type: ignore
from datetime import datetime

default_args = {
    "owner": "upi_pipeline",
    "start_date": datetime(2024, 1, 1),
}

with DAG(
    dag_id="upi_transaction_pipeline",
    default_args=default_args,
    schedule_interval="@hourly",
    catchup=False,
) as dag:

    run_etl = BashOperator(
    task_id="run_etl_pipeline",
    bash_command="cd /opt/airflow/project && python main.py"
)

    run_etl