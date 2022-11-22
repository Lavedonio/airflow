"""
    Email-related helper functions.
"""
from typing import Any


class EmailAux:

    @staticmethod
    def dag_success_callback(context: dict[str, Any]):
        print('Email callback')
        print(context)

    @staticmethod
    def task_success_callback(context: dict[str, Any]):
        print('Email callback')
        print(context)
