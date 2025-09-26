from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="mobile_pipeline",
    start_date=datetime(2025, 9, 25),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    run_script = BashOperator(
        task_id="fetch_logs",
        bash_command="source /home/gatitu/venv/bin/activate & python /home/gatitu/airflow/dags/mobile_pipeline.py"
    )