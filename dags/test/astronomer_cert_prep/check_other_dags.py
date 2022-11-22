"""
    This DAG is for practicing for the Astronomer DAG Authoring Certification.

    This DAG waits for the other astronomer_cert_prep tasks to finish.
"""
from datetime import datetime, timedelta

from airflow.operators.empty import EmptyOperator
from airflow.operators.python import ShortCircuitOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.utils.task_group import TaskGroup

from custom_operators.db.postgres import PostgresQueryOperator
from helper_modules.airflow import DefaultDAG
from helper_modules.project import SCRIPTS_PATHS


dags_list = [
    {
        "dag_id": "test_astronomer_cert_prep_check_other_dags",
        "is_paused": False
    },
    {
        "dag_id": "test_astronomer_cert_prep_dag_with_taskflow_api",
        "is_paused": False
    },
    {
        "dag_id": "test_astronomer_cert_prep_old_dag_format",
        "is_paused": False
    },
    {
        "dag_id": "test_astronomer_cert_prep_subdag",
        "is_paused": True
    },
    {
        "dag_id": "test_astronomer_cert_prep_task_group",
        "is_paused": False
    },
    {
        "dag_id": "test_first_dag",
        "is_paused": True
    },
]


with DefaultDAG(
    dag_path=__file__,
    docstring=__doc__,
    extra_tags=['Astronomer'],
    default_args={
        "start_date": datetime(2022, 7, 25, 0, 0),
        "retries": 1,
        "execution_timeout": timedelta(minutes=10),
    },
    description="DAG with TaskGroup for the Certification training",
    schedule_interval="0/10 * * * *",
    dagrun_timeout=timedelta(minutes=10),
    template_searchpath=str(SCRIPTS_PATHS['sql']),
) as dag:

    start = EmptyOperator(task_id='start')
    end = EmptyOperator(
        task_id='end',
        trigger_rule='none_failed_min_one_success',
        sla=timedelta(minutes=10)
    )

    get_active_dags = PostgresQueryOperator(
        task_id='get_active_dags',
        postgres_conn_id='airflow_db',
        sql='check_paused_dags.sql'
    )

    trigger_final_test = TriggerDagRunOperator(
        task_id='trigger_final_test',
        trigger_dag_id='test_first_dag',
        execution_date='{{ ds }}',
        wait_for_completion=True,
        poke_interval=30,
        reset_dag_run=True,
        failed_states=['failed'],
        trigger_rule='none_failed_min_one_success',
    )

    with TaskGroup(group_id='check_and_wait_for_dags') as check_and_wait_for_dags:
        for dag_info in dags_list:
            if dag_info['dag_id'].startswith('test_astronomer_cert_prep_') and dag_info["dag_id"] != dag.dag_id:
                check_if_dag_is_not_paused = ShortCircuitOperator(
                    task_id='check_if_dag_{dag_id}_is_not_paused'.format(**dag_info),
                    python_callable=lambda x: not x,
                    op_args=[dag_info['is_paused']],
                    ignore_downstream_trigger_rules=False,
                )

                wait_for_dag_to_finish = ExternalTaskSensor(
                    task_id='wait_for_dag_{dag_id}_to_finish'.format(**dag_info),
                    external_dag_id=dag_info["dag_id"],
                    external_task_id='end',
                    failed_states=['failed'],
                    allowed_states=['success', 'skipped']
                )

                check_if_dag_is_not_paused >> wait_for_dag_to_finish

    start >> get_active_dags >> check_and_wait_for_dags >> trigger_final_test >> end
