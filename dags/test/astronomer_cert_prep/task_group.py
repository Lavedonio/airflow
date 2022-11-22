"""
    This DAG is for practicing for the Astronomer DAG Authoring Certification.

    This is the new way of instanciating a DAG, with the TaskFlow API.

    This DAG is using the old way of grouping tasks, with SubDAG.
"""
import time
from datetime import datetime, timedelta

from airflow.decorators import task
from airflow.models import Variable
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import get_current_context
from airflow.sensors.date_time import DateTimeSensor
from airflow.utils.task_group import TaskGroup

from helper_modules.airflow import DefaultDAG

partners_list = [
    {
        "partner_name": "astronomer",
        "files_path": "/tmp/astronomer"
    },
    {
        "partner_name": "netflix",
        "files_path": "/tmp/netflix"
    },
    {
        "partner_name": "amazon",
        "files_path": "/tmp/amazon"
    },
    {
        "partner_name": "salesforce",
        "files_path": "/tmp/salesforce"
    },
    {
        "partner_name": "zendesk",
        "files_path": "/tmp/zendesk"
    }
]


@task.python(task_id='extract', multiple_outputs=True)
def _extract() -> dict[str, str]:
    var_info = Variable.get('test_astronomer_cert_prep_variable', deserialize_json=True)
    return var_info


@task.python(pool='test_astronomer_process_pool', priority_weight=1)
def process_a(first_name: str, surname: str) -> None:
    time.sleep(10)
    print(f"Full name: {first_name} {surname}")


@task.python(pool='test_astronomer_process_pool', priority_weight=2)
def process_b(first_name: str) -> None:
    time.sleep(15)
    print(f"First name: {first_name}")


@task.python(pool='test_astronomer_process_pool', priority_weight=3)
def process_c(surname: str) -> None:
    time.sleep(20)
    print(f"Surname: {surname}")


@task.branch
def choosing_partner() -> str:
    ds: str = get_current_context()['ds']
    schedule = {
        0: 'process_tasks.partners.process_astronomer',
        1: 'process_tasks.partners.process_netflix',
        2: 'process_tasks.partners.process_amazon',
        3: 'process_tasks.partners.process_salesforce',
        4: 'process_tasks.partners.process_zendesk',
    }
    day = datetime.strptime(ds, '%Y-%m-%d').weekday()
    try:
        return schedule[day]
    except KeyError:
        return 'end'



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
) as dag:

    start = EmptyOperator(task_id='start')
    end = EmptyOperator(
        task_id='end',
        trigger_rule='none_failed_min_one_success',
        sla=timedelta(minutes=10)
    )

    delay = DateTimeSensor(
        task_id='delay',
        target_time='{{ execution_date.add(minutes=12) }}',
        mode='reschedule',
        timeout=60 * 5,  # 5 minutes
        # soft_fail=True,
        exponential_backoff=True
    )

    extract_task = _extract()

    with TaskGroup(group_id='process_tasks') as process_tasks:
        with TaskGroup(group_id='airflow_variable') as airflow_variable:
            process_task_a = process_a(extract_task['first_name'], extract_task['surname'])
            process_task_b = process_b(extract_task['first_name'])
            process_task_c = process_c(extract_task['surname'])
        
        with TaskGroup(group_id='partners') as partners:
            for partner in partners_list:
                @task.python(task_id='process_{partner_name}'.format(**partner))
                def process(partner_name: str, files_path: str) -> None:
                    print(f"Partner name: {partner_name}")
                    print(f"Files path: {files_path}")

                process(**partner)
    
    choosing_partner_task = choosing_partner()

    start >> delay >> extract_task >> airflow_variable >> end
    extract_task >> choosing_partner_task >> [partners, end]
    partners >> end


