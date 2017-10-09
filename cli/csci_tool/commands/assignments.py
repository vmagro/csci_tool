"""Commands for viewing assignment data."""

import click

from .base import pass_api
from ..models import Assignment


@click.group()
def assignment():
    """Command group for assignments."""
    pass


@assignment.command()
@click.argument('course')
@pass_api
def list(api, course):
    """List all assignments in the database."""
    assignments = api.courses.assignments.list(course_pk=course)
    for a in assignments:
        a = Assignment(a)
        print(a)
