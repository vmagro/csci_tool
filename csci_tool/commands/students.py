"""Commands for interacting with student data."""

import click
import csv
import peewee

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
@click.option('--unix_name', prompt=True)
@click.option('--usc_id', prompt=True)
@click.option('--github_username', prompt=True)
@click.option('--preferred_name', prompt=True)
@click.option('--first_name', prompt=True)
@click.option('--last_name', prompt=True)
def create(unix_name, usc_id, github_username, preferred_name, first_name, last_name):
    """Add a new student to the db and create their repo."""
    student = Student(
        unix_name=unix_name,
        usc_id=usc_id,
        github_username=github_username,
        preferred_name=preferred_name,
        first_name=first_name,
        last_name=last_name,
    )
    try:
        student.save()
        click.echo('Created: {}'.format(student))
    except peewee.IntegrityError as e:
        e = e.__str__()
        if 'UNIQUE constraint failed' in e:
            # hacky way to get the field that wasn't unique
            field = e[e.rfind('.')+1:]
            click.secho('Failed to create {}: {} already exists'.format(student, field), fg='red')
        else:
            click.secho('Failed to create {} - unknown error'.format(student), fg='red')


@student.command()
@click.argument('csv_file', type=click.File('r'))
@click.pass_context
def create_bulk(ctx, csv_file):
    """Bulk add students from a CSV file."""
    reader = csv.DictReader(csv_file)
    # make sure that the field names are appropriate
    fields = ['Unix Name', 'USC ID', 'GitHub Username', 'Preferred Name', 'First Name', 'Last Name']
    present = [f.replace(' ', '_').lower() for f in reader.fieldnames]
    for field in fields:
        processed = field.replace(' ', '_').lower()
        assert processed in present, 'Missing field "{}"'.format(field)

    for line in reader:
        # convert to our required keys
        line = {k.replace(' ', '_').lower(): v for k, v in line.items()}
        ctx.invoke(create, **line)
