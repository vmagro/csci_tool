"""Tasks for deploying an assignment to student repos."""
from typing import Type, List
import os

from celery import shared_task, chain, group
from celery.utils.log import get_task_logger

from .models import Student, Assignment, Mutation
from .repo import LocalRepo
from . import assignment_utils

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
def mutate_repo(repo: Type[LocalRepo], assignment: Type[Assignment], student: Type[Student]
                ) -> (Type[LocalRepo], str):
    """Mutate a repo by running mutate.py in the given directory.

    Returns:
        (repo, commit message)

    """
    logger.info('Importing mutation for %s', assignment.name)
    # use the Assignment to find out where it lives on disk
    base_path = assignment.course.settings().assignments_repo_path
    assignment_path = os.path.join(base_path, assignment.path)
    # import the mutation function
    mutate = assignment_utils.import_mutate(assignment_path)
    logger.info('Applying mutation')
    # make the destination directory
    dest_dir = os.path.join(repo.path, assignment.name)
    os.makedirs(dest_dir, exist_ok=True)
    # we want to have cwd be the destination directory in the student's repo
    cwd = os.getcwd()
    os.chdir(dest_dir)
    # perform the mutation
    commit_message = mutate(student, assignment_path)
    # go back to original working dir
    os.chdir(cwd)
    logger.info('Applied mutation')
    logger.debug('Commit message: %s', commit_message)
    return (repo, commit_message)


@shared_task
def commit_repo(repo_and_commit: (Type[LocalRepo], str), assignment: Type[Assignment],
                student: Type[Student]) -> Type[LocalRepo]:
    """Add all local files and commit any changes to the repo."""
    repo, commit_message = repo_and_commit
    logger.info('Committing repo at %s', repo.path)
    # get the bot username and email from the course settings
    settings = student.course.settings()
    sha = repo.commit(settings.bot_username, settings.bot_email, commit_message)
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
                 mutate_repo.s(assignment, student),
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
