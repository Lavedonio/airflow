"""
    This DAG is for practicing for the Astronomer DAG Authoring Certification.

    This is the new way of instanciating a DAG, with the TaskFlow API.
"""
from datetime import datetime, timedelta

from airflow.decorators import task
from airflow.models import Variable
from airflow.operators.empty import EmptyOperator

from helper_modules.airflow import DefaultDAG


@task.python(task_id='extract', multiple_outputs=True)
def _extract() -> dict[str, str]:
    var_info = Variable.get('test_astronomer_cert_prep_variable', deserialize_json=True)
    return var_info


@task.python
def process(first_name: str, surname: str) -> None:
    print(f"{first_name} {surname}")


with DefaultDAG(
    dag_path=__file__,
    docstring=__doc__,
    extra_tags=['Astronomer'],
    default_args={
        "start_date": datetime(2022, 7, 24, 0, 0),
        "retries": 1,
    },
    description="Second DAG from the Certification training",
    schedule_interval="0/10 * * * *",
    dagrun_timeout=timedelta(minutes=10),
) as dag:

    start = EmptyOperator(task_id='start')
    end = EmptyOperator(task_id='end')

    extract_task = _extract()
    process_task = process(extract_task['first_name'], extract_task['surname'])

    start >> extract_task >> process_task >> end
