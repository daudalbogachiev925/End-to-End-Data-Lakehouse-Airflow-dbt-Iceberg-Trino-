from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    "owner": "data-eng",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="bronze_ingest",
    start_date=days_ago(1),
    schedule="0 * * * *",
    catchup=False,
    default_args=default_args,
    tags=["bronze", "spark"],
) as dag:

    seed = DockerOperator(
        task_id="seed_raw_data",
        image="python:3.11-slim",
        command="pip install -q faker boto3 && python /scripts/seed_data.py",
        docker_url="unix://var/run/docker.sock",
        network_mode="lakehouse-ecommerce_default",
        mounts=[{"source": "/absolute/path/scripts", "target": "/scripts", "type": "bind"}],
        auto_remove=True,
    )

    ingest = DockerOperator(
        task_id="spark_iceberg_write",
        image="bitnami/spark:3.5",
        command="spark-submit /opt/spark/jobs/iceberg_writer.py",
        docker_url="unix://var/run/docker.sock",
        network_mode="lakehouse-ecommerce_default",
        mounts=[{"source": "/absolute/path/spark", "target": "/opt/spark/jobs", "type": "bind"}],
        auto_remove=True,
    )

    seed >> ingest
