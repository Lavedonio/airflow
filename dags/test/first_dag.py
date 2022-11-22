"""
    This DAG is only used to test new features in Airflow.
"""

# Python imports
import time
from datetime import datetime, timedelta

# Airflow imports
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

# Project imports
from helper_modules.airflow import DAGParameters


dag_params = DAGParameters(__file__)

dag_id = dag_params.generate_dag_id()
tags = dag_params.generate_default_tags()

default_args = {
    "owner": "Daniel Lavedonio de Lima",
    "start_date": datetime(2021, 3, 14, 0, 0),
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email": ["daniel.lavedonio@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False
}

dag = DAG(dag_id,
          schedule_interval="0 12 * * *",
          tags=tags,
          default_args=default_args,
          catchup=False)
dag.doc_md = __doc__


def sleep_for(seconds: float) -> None:
    print(f'Sleeping for {seconds:.2f} seconds...')
    time.sleep(seconds)
    print('Waking up!')


task_1 = EmptyOperator(task_id='task_1', dag=dag)
task_2 = PythonOperator(task_id='task_2', python_callable=sleep_for, op_args=[20], dag=dag)
task_3 = EmptyOperator(task_id='task_3', dag=dag)

task_1 >> task_2 >> task_3
