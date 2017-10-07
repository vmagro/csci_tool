"""Tasks for collecting assignments from student repos."""
from typing import Type, List
from celery import shared_task, group
from celery.utils.log import get_task_logger

from .models import Student, Assignment, Submission

logger = get_task_logger(__name__)


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
