"""Tasks for working with the assignments/meta repo."""
import os
from os import path
from typing import Type
from celery import shared_task
from celery.utils.log import get_task_logger

from .models import Assignment, Course
from .repo import LocalRepo
from .assignment_utils import assignment_status

logger = get_task_logger(__name__)


@shared_task
def update_assignment_repo(course: Type[Course]) -> Type[LocalRepo]:
    """Update to or clone the latest version of the assigments repo."""
    repo_path = course.settings().assignments_repo_path
    settings = course.settings()
    if path.exists(repo_path):
        logger.info('Assignments repo exists already, pulling any changes')
        repo = LocalRepo(settings.assignments_repo_path)
        repo.pull()
    else:
        logger.info('Assignments repo does not exist, cloning it now')
        repo = LocalRepo.clone_from_url(settings.assignments_repo_url,
                                        settings.assignments_repo_path)
    return repo


@shared_task
def look_for_assignments(repo: Type[LocalRepo]):
    """Look for assignments (directories with mutate.py) in the repo and save them to db."""
    found = []
    for d in os.listdir(repo.path):
        full = path.join(repo.path, d)
        if path.isdir(full):
            if 'mutate.py' in list(os.listdir(full)):
                found.append(d)
    for directory in found:
        # check if the assignment exists already in the db
        try:
            assignment = Assignment.get(pk=directory)
            logger.info('Assignment "%s" already exists', directory)
            # the due date might still have been changed, let's update it just in case
            logger.info('Updating %s due date', directory)
            due_date = open(path.join(repo.path, directory, 'due_date.txt'), 'r').read()
            assignment.due_date = due_date
        except:
            # doesn't exist, lets create it
            # read the due date from a file in the directory
            due_date = open(path.join(repo.path, directory, 'due_date.txt'), 'r').read()
            logger.info('Creating new assignment %s, due on %s', directory, due_date)
            assignment = Assignment(path=directory, due_date=due_date)
        # now the assignment exists for sure, make the status string
        assignment.status = assignment_status(path.join(repo.path, directory))
        assignment.save()

    # check if there are any assignments that we need to delete
    for assignment in Assignment.objects.all():
        if assignment.path not in found:
            logger.info('Assignment %s no longer exists, deleting it', assignment.path)
            assignment.delete()

    return found
