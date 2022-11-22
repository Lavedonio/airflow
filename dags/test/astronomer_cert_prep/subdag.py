"""
    This DAG is for practicing for the Astronomer DAG Authoring Certification.

    This is the new way of instanciating a DAG, with the TaskFlow API.

    This DAG is using the old way of grouping tasks, with SubDAG.
"""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.models import Variable, TaskInstance
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import get_current_context

from helper_modules.airflow.dags import DAGParameters
from helper_modules.airflow.subdags import DefaultSubDagOperator


dag_params = DAGParameters(__file__)

dag_id = dag_params.generate_dag_id()
tags = dag_params.generate_default_tags(extra_tags=['Astronomer'])
default_args = dag_params.generate_default_args(default_args={
    "start_date": datetime(2022, 7, 25, 0, 0),
    "retries": 1,
})


@task.python(task_id='extract')
def _extract() -> dict[str, str]:
    var_info = Variable.get('test_astronomer_cert_prep_variable', deserialize_json=True)
    return var_info


@task.python
def process_a() -> None:
    ti: TaskInstance = get_current_context()['ti']
    var_info = ti.xcom_pull(key='return_value', task_ids='extract', dag_id=dag_id)
    print("First name: {first_name}".format(**var_info))


@task.python
def process_b() -> None:
    ti: TaskInstance = get_current_context()['ti']
    var_info = ti.xcom_pull(key='return_value', task_ids='extract', dag_id=dag_id)
    print("Surname: {surname}".format(**var_info))


@task.python
def process_c() -> None:
    ti: TaskInstance = get_current_context()['ti']
    var_info = ti.xcom_pull(key='return_value', task_ids='extract', dag_id=dag_id)
    print("Full name: {first_name} {surname}".format(**var_info))


with DAG(dag_id,
         description="DAG with SubDAG for the Certification training",
         schedule_interval="0/10 * * * *",
         dagrun_timeout=timedelta(minutes=10),
         tags=tags,
         default_args=default_args,
         catchup=False) as dag:
    dag.doc_md = __doc__

    start = EmptyOperator(task_id='start')
    end = EmptyOperator(task_id='end')

    extract_task = _extract()

    process_tasks = DefaultSubDagOperator(
        subdag_id='process_tasks',
        dag=dag,
        tasks=[process_a, process_b, process_c]
    )

    start >> extract_task >> process_tasks >> end
