"""Writes partitioned output. Its context use is indirect, so it needs a human (or Claude)."""
import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import CronDataIntervalTimetable


def _partition_path(ctx):
    # `ctx` is the task context, but only the caller knows that
    return ctx["execution_date"].strftime("%Y/%m/%d")


def write(**context):
    print("writing", _partition_path(context))


with DAG("partitions", schedule=CronDataIntervalTimetable("@hourly", timezone="UTC"), start_date=datetime.datetime(2024, 1, 1), catchup=False) as dag:
    PythonOperator(task_id="write", python_callable=write) >> BashOperator(
        task_id="next_window", bash_command="echo next window starts {{ next_ds }}"
    )
