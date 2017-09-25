"""Commands for viewing assignment data."""

import click

from .base import pass_api
from ..models import Assignment


@click.group()
def assignment():
    """Command group for assignments."""
    pass


@assignment.command()
@pass_api
def list(api):
    """List all students in the database."""
    assignments = api.assignments.list()
    for a in assignments:
        a = Assignment(a)
        print(a)
