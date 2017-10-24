"""Tasks for collecting assignments from student repos."""
from typing import Type, List
import logging

from ..models import Student, Assignment, Submission

logger = logging.getLogger(__name__)


def collect_assignment(student: Type[Student], assignment: Type[Assignment]):
    """Save a Submission object tying a Student Commit to the given Assignment."""
    commit = student.repo.head_commit()
    logger.info('Latest commit for %s: %s', student.unix_name, commit.sha)
    submission = Submission(student=student, assignment=assignment, commit=commit)
    submission.save()

    # comment on this commit on GitHub
    repo = student.repo.github()
    commit = repo.get_commits(commit.sha)[0]
    message = student.course.settings().collect_comment
    message = message.format(assignment.name)
    commit.create_comment(message)


def collect_assignment_from_all(students: List[Student], assignment: Type[Assignment]):
    """Collect an Assignment from a list of students."""
    collect_tasks = [collect_assignment.s(student, assignment) for student in students]
    g = group(collect_tasks)
    return g.apply_async()
