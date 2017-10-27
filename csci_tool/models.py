"""Data models for csci_tool."""
from peewee import Model, CharField, DateTimeField, ForeignKeyField
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime
import atexit
import os

from .course_settings import CourseSettings

# just use an in-memory database so that we don't have git versioning issues
# the database will be re-populated from a sql dump every run - the sql dump is easily diff-able
db = SqliteExtDatabase(':memory:')


class BaseModel(Model):
    class Meta:
        database = db


class Student(BaseModel):
    usc_id = CharField(unique=True)
    unix_name = CharField(unique=True)
    github_username = CharField(unique=True)
    first_name = CharField()
    last_name = CharField()
    preferred_name = CharField()

    @property
    def usc_email(self):
        """Get the email of the student from their unix name."""
        return self.unix_name + '@usc.edu'

    @property
    def repo_name(self):
        """Get a string name for the student's repo."""
        # TODO is there a less gross way to do this?
        fields = self._data
        return CourseSettings.get_settings().student_repo_format.format(**fields).lower()

    @property
    def repo_url(self):
        """Get a cloneable URL to the student's GitHub repo."""
        settings = CourseSettings.get_settings()
        return 'https://{}:{}@github.com/{}/{}.git'.format(
            settings.bot_username, settings.bot_token, settings.github_org, self.repo_name
        )


class Assignment(BaseModel):
    path = CharField(unique=True)
    status = CharField()


class Submission(BaseModel):
    sha = CharField(unique=True)
    student = ForeignKeyField(Student, related_name='submissions')
    assignment = ForeignKeyField(Assignment, related_name='assignments')
    date_collected = DateTimeField(default=datetime.datetime.now)
    num_late_days = DateTimeField(default=0)


class Mutation(BaseModel):
    student = ForeignKeyField(Student, related_name='mutations')
    assignment = ForeignKeyField(Assignment, related_name='mutations')
    date_performed = DateTimeField(default=datetime.datetime.now)


db.connect()

# load the sql dump if we have one
if os.path.exists('database.sql'):
    with open('database.sql', 'r') as f:
        sql = f.read()
        db.get_conn().executescript(sql)
else:
    # if we don't have a database dump, then its safe to create the tables
    db.create_tables([Student, Assignment, Submission, Mutation])


# save the SQL dump at the end of program execution
def save_dump():
    """Save the sql dump to a file so it can be easier tracked in git."""
    with open('database.sql', 'w') as f:
        for line in db.get_conn().iterdump():
            f.write('%s\n' % line)


atexit.register(save_dump)
