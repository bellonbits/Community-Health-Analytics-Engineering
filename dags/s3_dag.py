from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="chw_data_minio",
    start_date=datetime(2025, 9, 25),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    run_script = BashOperator(
        task_id="fetch_csv",
        bash_command="source /home/gatitu/venv/bin/activate & python /home/gatitu/airflow/dags/data_s3.py"
    )