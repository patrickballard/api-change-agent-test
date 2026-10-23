"""Daily ETL, written for Airflow 2."""
import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import CronDataIntervalTimetable


def extract(**context):
    run_date = context["logical_date"]  # the run's logical date
    print(f"extracting for {run_date:%Y-%m-%d}")
    return run_date.strftime("%Y-%m-%d")


def load(**kwargs):
    day = kwargs.get("logical_date")
    print("loading", day, "after", kwargs["macros"].ds_add(kwargs["ds"], -1))


def summarize(templates_dict, **_):
    print(templates_dict["query"])


with DAG(
    dag_id="etl_daily",
    schedule=CronDataIntervalTimetable("@daily", timezone="UTC"),
    start_date=datetime.datetime(2024, 1, 1),
    catchup=False,
) as dag:
    extract_task = PythonOperator(task_id="extract", python_callable=extract)
    load_task = PythonOperator(task_id="load", python_callable=load)
    report = BashOperator(
        task_id="report",
        bash_command="echo report for {{ logical_date }} after {{ macros.ds_add(ds, -1) }}",
    )
    script = BashOperator(task_id="script", bash_command="scripts/report.sh")
    summary = PythonOperator(
        task_id="summary",
        python_callable=summarize,
        templates_dict={"query": "sql/summary.sql"},
        templates_exts=[".sql"],
    )
    extract_task >> load_task >> [report, script, summary]
