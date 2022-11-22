"""
    DAG-related helper functions.
"""
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from airflow import DAG


def dag_success_callback(context: dict[str, Any]):
    print(context)


def dag_failure_callback(context: dict[str, Any]):
    print(context)


def sla_miss_callback(dag, task_list, blocking_task_list, slas, blocking_tis):
    print(dag)
    print(task_list)
    print(blocking_task_list)
    print(slas)
    print(blocking_tis)


DEFAULT_DAG_ARGS = {
    "owner": "Daniel Lavedonio de Lima",
    "start_date": datetime(2022, 1, 1, 0, 0),
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "retry_exponential_backoff": False,
    "max_retry_delay": timedelta(minutes=15),
    "sla": timedelta(hours=1),
    "email": ["daniel.lavedonio@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    # "on_success_callback": success_callback,
    # "on_failure_callback": failure_callback,
}


class DAGParameters:
    """
        Contains all DAG default parameter generation methods.
    """

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def generate_dag_id(self) -> str:
        """
            Generate a dag_id based on the file path inside the dags folder.
            This garanties that the dag_id will be unique and that it will
            match with its current location.
        """
        path_in_parts = Path(self.file_path).resolve().parts
        path_after_dags_folder = path_in_parts[path_in_parts.index('dags')+1:]
        dag_id = '_'.join(path_after_dags_folder).replace('.py', '')
        return dag_id

    def generate_default_tags(self, extra_tags: list[str] | None = None) -> list[str]:
        """
            Generate a default tags list containing the folders in which
            the DAG is located.
        """
        if extra_tags is None:
            extra_tags = []

        path_in_parts = list(Path(self.file_path).resolve().parts)
        default_tags = path_in_parts[path_in_parts.index('dags')+1:-1]

        return default_tags + extra_tags
    
    def generate_default_args(self, default_args: dict[str, Any] | None = None) -> dict[str, Any]:
        """
            Generate the default_args parameter based on the DEFAULT_DAG_ARGS defined above.
            
            The parameter :default_args overrides any config already set in DEFAULT_DAG_ARGS.
        """
        if default_args is None:
            default_args = {}
        
        return {**DEFAULT_DAG_ARGS, **default_args}
    
    def get_all_default_parameters(
        self,
        extra_tags: list[str] | None = None,
        default_args: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
            Generate all the default parameters at once and return a
            dictionary with all of them.
        """
        all_params = {
            'dag_id': self.generate_dag_id(),
            'tags': self.generate_default_tags(extra_tags),
            'default_args': self.generate_default_args(default_args),
        }
        return all_params


class DefaultDAG(DAG):

    def __init__(self,
        dag_path: str,
        catchup: bool = False,
        docstring: str | None = None,
        extra_tags: list[str] | None = None,
        default_args: dict[str, Any] | None = None,
        **kwargs
    ):
        if default_args is None:
            default_args = {}

        if extra_tags is None:
            extra_tags = []

        self.docstring = docstring

        dag_params = DAGParameters(dag_path)

        super().__init__(
            **dag_params.get_all_default_parameters(extra_tags, default_args),
            catchup=catchup,
            on_success_callback=dag_success_callback,
            on_failure_callback=dag_failure_callback,
            sla_miss_callback=sla_miss_callback,
            **kwargs
        )

    def __enter__(self):
        dag = super().__enter__()
        if self.docstring is not None:
            dag.doc_md = self.docstring
        return dag
