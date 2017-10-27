"""Commands for viewing assignment data."""

import click

from ..models import Assignment


@click.group()
def assignment():
    """Command group for assignments."""
    pass


@assignment.command()
@click.argument('course')
def list(api, course):
    """List all assignments in the database."""
    assignments = api.courses.assignments.list(course_pk=course)
    for a in assignments:
        a = Assignment(a)
        print(a)


@assignment.command()
@click.argument('course')
@click.argument('assignment')
@click.option('--canary/--no-canary', default=False, prompt=True)
def deploy(api, course, assignment, canary):
    """Deploy assignment to students - either all or subset where canary=True."""
    response = api.courses.assignments.deploy(course_pk=course, assignment=assignment,
                                              canary=canary, validate=False)
    print(response)


@assignment.command()
@click.argument('course')
@click.argument('assignment')
@click.option('--canary/--no-canary', default=False, prompt=True)
def collect(api, course, assignment, canary):
    """Collect assignment from students - either all or subset where canary=True."""
    response = api.courses.assignments.collect(course_pk=course, assignment=assignment,
                                               canary=canary, validate=False)
    print(response)
