"""Commands for interacting with student data."""

import click

from ..models import Student


@click.group()
def student():
    """Command group for students."""
    pass


@student.command()
def list():
    """List all students in the database."""
    students = Student.select()
    for s in students:
        print(s)


@student.command()
@click.option('--unixname', prompt=True)
@click.option('--usc_id', prompt=True)
@click.option('--github_username', prompt=True)
@click.option('--preferred_name', prompt=True)
@click.option('--first_name', prompt=True)
@click.option('--last_name', prompt=True)
def create(unixname, usc_id, github_username, preferred_name, first_name, last_name):
    """Add a new student to the db."""
    student = Student(
        unix_name=unixname,
        usc_id=usc_id,
        github_username=github_username,
        preferred_name=preferred_name,
        first_name=first_name,
        last_name=last_name,
    )
    student.save()
    print(student)
