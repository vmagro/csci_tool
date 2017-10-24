"""Commands for interacting with student data."""

import click

from .base import pass_config
from ..models import Student


@click.group()
def student():
    """Command group for students."""
    pass


@student.command()
@pass_config
def list(api):
    """List all students in the database."""
    students = api.students.list()
    for s in students:
        s = Student(s)
        print(s)


@student.command()
@click.argument('usc_email')
@click.argument('usc_id')
@click.argument('github_username')
@click.argument('preferred_name')
@click.argument('first_name')
@click.argument('last_name')
@pass_config
def create(config, usc_email, usc_id, github_username, preferred_name, first_name, last_name):
    """Add a new student to the db."""
    try:
        student = api.students.create(
            usc_email=usc_email,
            usc_id=usc_id,
            github_username=github_username,
            preferred_name=preferred_name,
            first_name=first_name,
            last_name=last_name,
        )
        student = Student(student)
        print(student)
    except Exception as e:
        if hasattr(e, 'error'):
            if 'github_username' in e.error:
                messages = e.error['github_username']
                click.secho('\n'.join(messages), fg='red')
            else:
                # loop over all the keys, join all the messages
                messages = []
                for field in e.error:
                    # e.error.field is a list of messages explaining all the issues
                    messages += e.error[field]
                messages = '\n'.join(messages)
                click.secho(messages, fg='red')
        else:
            click.secho('An unknown error occurred.', fg='red')
            raise
