"""
    SubDAG-related helper functions.
"""
from dataclasses import dataclass
from typing import Any, Callable

from airflow import DAG, AirflowException
from airflow.decorators.python import _PythonDecoratedOperator
from airflow.operators.python import PythonOperator
from airflow.operators.subdag import SubDagOperator


@dataclass
class PythonOperatorInfoForSubDag:
    task_id: str
    python_callable: Callable
    kwargs: dict[str, Any] | None


def subdag_factory(
    subdag_id: str,
    dag: DAG,
    tasks: list[_PythonDecoratedOperator | PythonOperatorInfoForSubDag]
) -> DAG:
    assert isinstance(tasks, list), "tasks paramater must be a list."
    assert len(tasks) > 0, "List can not be empty."

    with DAG(f'{dag.dag_id}.{subdag_id}', default_args=dag.default_args) as subdag:
        for task in tasks:
            if isinstance(task, PythonOperatorInfoForSubDag):
                PythonOperator(
                    task_id=task.task_id,
                    python_callable=task.python_callable,
                    op_kwargs=task.kwargs
                )
            else:
                try:
                    task()
                except Exception:
                    raise AirflowException('Unexpected task info type.')
    
    return subdag


class DefaultSubDagOperator(SubDagOperator):

    def __init__(self, *, subdag_id: str, dag: DAG,
                tasks: list[_PythonDecoratedOperator | PythonOperatorInfoForSubDag],
                **kwargs) -> None:

        task_id = subdag_id
        subdag = subdag_factory(subdag_id, dag, tasks)
        super().__init__(subdag=subdag, task_id=task_id, **kwargs)
