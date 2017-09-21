"""Celery tasks for gitbot."""
from typing import Type
from celery import shared_task, chain
from celery.utils.log import get_task_logger

from .models import Student, Assignment
from .repo import LocalRepo

logger = get_task_logger(__name__)


@shared_task
def clone_repo(student: Type[Student]) -> Type[LocalRepo]:
    """Clones a repo for a Student."""
    logger.info('Cloning repo for %s', student)
    repo_stub = student.repo
    local_repo = LocalRepo.clone_repo(repo_stub)
    logger.info('Cloned repo for %s to %s', student, local_repo.path)
    return local_repo


@shared_task
def mutate_repo(repo: Type[LocalRepo], assignment: Type[Assignment]) -> (Type[LocalRepo], str):
    """Mutate a repo by running mutate.py in the given directory.

    Returns:
        (repo, commit message)

    """
    logger.info('Importing mutation for %s', assignment.name)
    logger.info('Applying mutation')
    logger.info('Applied mutation')
    commit_message = 'My super awesome commit message'
    logger.debug('Commit message: %s', commit_message)
    return (repo, commit_message)


@shared_task
def commit_repo(repo_and_commit: (Type[LocalRepo], str)) -> Type[LocalRepo]:
    """Add all local files and commit any changes to the repo."""
    repo, commit_message = repo_and_commit
    logger.info('Committing repo at %s', repo.path)
    return repo


@shared_task
def push_repo(repo: Type[LocalRepo]):
    """Push new repo commit to GitHub."""
    logger.info('Pushing repo at %s to GitHub', repo.path)
    return repo


def update_repo(student: Type[Student], assignment: Type[Assignment]):
    """Update a repo given an assignment. clone -> mutate -> commit -> push."""
    update_chain = chain(clone_repo.s(student), mutate_repo.s(assignment),
                         commit_repo.s(), push_repo.s())
    return update_chain.apply_async()
