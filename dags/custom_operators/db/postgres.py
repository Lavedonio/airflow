"""
    Module containing custom operators based on
    airflow.providers.postgres.operators.postgres module.
"""
from typing import Any

from airflow.providers.postgres.operators.postgres import PostgresOperator


class PostgresQueryOperator(PostgresOperator):
    """
        Run a query in a Postgres database and return the results.
    """

    def execute(self, context: dict[str, Any]):
        return super().execute(context)
