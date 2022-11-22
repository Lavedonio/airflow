"""
    Tasks-related helper functions.
"""
from typing import Any
from helper_modules.airflow._empty_callback import empty_callback
from helper_modules.messaging import EmailAux, SlackAux


def task_success_callback(slack=False, email=False):
    email_callback = EmailAux.task_success_callback if email else empty_callback
    slack_callback = SlackAux.task_success_callback if slack else empty_callback

    def final_task_success_callback(context: dict[str, Any]):
        slack_callback()
        email_callback()
    
    return final_task_success_callback


def task_failure_callback(context):
    print(context)


def task_retry_callback(context):
    print(context)


def task_execute_callback(context):
    print(context)
