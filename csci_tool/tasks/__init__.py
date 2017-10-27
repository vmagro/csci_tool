"""Celery tasks for gitbot."""

# import all the other tasks files so that celery can find them
from .collect_tasks import * # noqa
from .deploy_tasks import * # noqa
