"""Celery tasks for gitbot."""
import os
from os import path
from typing import Type, List
from celery import shared_task, chain, group
from celery.utils.log import get_task_logger

from .app_settings import (
    BOT_USERNAME as author_name, BOT_EMAIL as author_email,
    ASSIGNMENTS_REPO_URL, ASSIGNMENTS_REPO_PATH
)
from .models import Student, Assignment, Submission, Mutation
from .repo import LocalRepo
from .assignment_utils import assignment_status

logger = get_task_logger(__name__)


@shared_task
def update_assignment_repo() -> Type[LocalRepo]:
    """Update to or clone the latest version of the assigments repo."""
    if path.exists(ASSIGNMENTS_REPO_PATH):
        logger.info('Assignments repo exists already, pulling any changes')
        repo = LocalRepo(ASSIGNMENTS_REPO_PATH)
        repo.pull()
    else:
        logger.info('Assignments repo does not exist, cloning it now')
        repo = LocalRepo.clone_from_url(ASSIGNMENTS_REPO_URL, ASSIGNMENTS_REPO_PATH)
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
def commit_repo(repo_and_commit: (Type[LocalRepo], str), assignment: Type[Assignment],
                student: Type[Student]) -> Type[LocalRepo]:
    """Add all local files and commit any changes to the repo."""
    repo, commit_message = repo_and_commit
    logger.info('Committing repo at %s', repo.path)
    sha = repo.commit(author_name, author_email, commit_message)
    mutation = Mutation(student=student, sha=sha, assignment=assignment)
    mutation.save()
    return repo


@shared_task
def push_repo(repo: Type[LocalRepo]):
    """Push new repo commit to GitHub."""
    logger.info('Pushing repo at %s to GitHub', repo.path)
    repo.push()
    logger.info('Pushed repo to GitHub')
    return repo


@shared_task
def cleanup_repo(repo: Type[LocalRepo]):
    """Delete the files of a repo from disk when we're done with it."""
    repo.delete()


@shared_task
def give_assignment(student: Type[Student], assignment: Type[Assignment]):
    """Update a repo given an assignment. clone -> mutate -> commit -> push."""
    task = chain(clone_repo.s(student),
                 mutate_repo.s(assignment),
                 commit_repo.s(assignment, student),
                 push_repo.s(),
                 cleanup_repo.s(),
                 )

    return task.apply_async()


@shared_task
def give_assignment_to_all(students: List[Student], assignment: Type[Assignment]):
    """Update a list of students's repos using the mutation from an assignment."""
    give_tasks = [give_assignment.s(student, assignment) for student in students]
    g = group(give_tasks)
    return g.apply_async()


@shared_task
def collect_assignment(student: Type[Student], assignment: Type[Assignment]):
    """Save a Submission object tying a Student Commit to the given Assignment."""
    commit = student.repo.head_commit()
    logger.info('Latest commit for %s: %s', student.unix_name, commit.sha)
    submission = Submission(student=student, assignment=assignment, commit=commit)
    submission.save()
    # TODO comment on the commit so the student knows we collected it


@shared_task
def collect_assignment_from_all(students: List[Student], assignment: Type[Assignment]):
    """Collect an Assignment from a list of students."""
    collect_tasks = [collect_assignment.s(student, assignment) for student in students]
    g = group(collect_tasks)
    return g.apply_async()
