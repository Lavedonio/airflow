"""
    Slack-related helper functions.
"""
from typing import Any


class SlackAux:

    @staticmethod
    def dag_success_callback(context: dict[str, Any]):
        print('Slack callback')
        print(context)

    @staticmethod
    def task_success_callback(context: dict[str, Any]):
        print('Slack callback')
        print(context)
