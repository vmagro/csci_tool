"""Commands for interacting with student data."""

import click

from ..student import Student


@click.group()
def student():
    """Command group for students."""
    pass


@student.command()
def list():
    """List all students in the database."""
    students = Student.objects.all()
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
def create(usc_email, usc_id, github_username, preferred_name, first_name, last_name):
    """Add a new student to the db."""
    student = Student(
        usc_email=usc_email,
        usc_id=usc_id,
        github_username=github_username,
        preferred_name=preferred_name,
        first_name=first_name,
        last_name=last_name,
    )
    student.save()
    print(student)
