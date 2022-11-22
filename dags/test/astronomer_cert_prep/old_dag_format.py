"""
    This DAG is for practicing for the Astronomer DAG Authoring Certification.

    This is the old way of instanciating a DAG.
"""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.models import TaskInstance, Variable
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator


from helper_modules.airflow import DAGParameters
from helper_modules.project import SCRIPTS_PATHS


dag_params = DAGParameters(__file__)

dag_id = dag_params.generate_dag_id()
tags = dag_params.generate_default_tags(extra_tags=['Astronomer'])
default_args = dag_params.generate_default_args(default_args={
    "start_date": datetime(2022, 7, 24, 0, 0),
    "retries": 1,
})


def _get_info(first_name: str) -> None:
    print(first_name)


def _extract(ti: TaskInstance) -> None:
    var_info = Variable.get('test_astronomer_cert_prep_variable', deserialize_json=True)
    ti.xcom_push(key='var_info', value=var_info)


def _process(ti: TaskInstance) -> None:
    var_info: dict[str, str] = ti.xcom_pull(key='var_info', task_ids='extract')
    print("Full name: {first_name} {surname}".format(**var_info))


with DAG(dag_id,
         description="First DAG from the Certification training",
         schedule_interval="0/10 * * * *",
         dagrun_timeout=timedelta(minutes=10),
         tags=tags,
         default_args=default_args,
         catchup=False) as dag:
    dag.doc_md = __doc__

    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')

    task1 = DummyOperator(task_id='task1')

    task2 = BashOperator(
        task_id='task2',
        bash_command=str(SCRIPTS_PATHS['bash'] / 'basic_test.sh ')
    )

    task3 = PythonOperator(
        task_id='task3',
        python_callable=_get_info,
        op_args=['{{ var.json.test_astronomer_cert_prep_variable.first_name }}']
    )

    start >> task1 >> task2 >> task3 >> end

    extract = PythonOperator(
        task_id='extract',
        python_callable=_extract
    )

    process = PythonOperator(
        task_id='process',
        python_callable=_process
    )

    start >> extract >> process >> end
