"""
    This DAG is only used to test new features in Airflow.
"""

# Python imports
from datetime import datetime, timedelta

# Airflow imports
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator


default_args = {
    "owner": "Daniel Lavedonio de Lima",
    "start_date": datetime(2021, 3, 14, 0, 0),
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email": ["daniel.lavedonio@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False
}

dag = DAG('test_dag',
          schedule_interval="0 12 * * *",
          default_args=default_args,
          catchup=False)
dag.doc_md = __doc__


task_1 = DummyOperator(task_id='task_1', dag=dag)
