"""Database models supporting the gitbot application."""

from django.db import models

from .app_settings import GITHUB_ORG


class Student(models.Model):
    """A Student with a repo that we will give/collect assignments to/from."""

    usc_email = models.EmailField(primary_key=True)
    usc_id = models.CharField(max_length=20)
    github_username = models.CharField(max_length=100)
    preferred_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    @property
    def unix_name(self):
        """USC username extraced from email."""
        return self.usc_email[:-len('@usc.edu')]

    def __str__(self):
        """Return human-readable representation."""
        return 'Student: {} {} {}'.format(self.unix_name, self.first_name, self.last_name)


class Repo(models.Model):
    """A Student GitHub repo."""

    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, primary_key=True)

    def repo_url(self):
        """Cloneable URL to a REPO."""
        return 'git@github.com:{}/{}.git'.format(GITHUB_ORG, self.repo_name)

    def head_commit(self):
        """Get whatever the latest commit is to this repo at the current point in time."""
        return self.commit_set.order_by('-commit_date').first()

    def __str__(self):
        """Return human-readable representation."""
        return 'Repo: {} for {}'.format(self.name, self.student)


class Commit(models.Model):
    """Commit that is either a user commit or a bot commit."""

    sha = models.CharField(max_length=200, primary_key=True)
    author = models.CharField(max_length=100)
    commit_date = models.DateTimeField()
    push_date = models.DateTimeField()
    message = models.CharField(max_length=200)
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)


class Assignment(models.Model):
    """An Assignment is a directory in the meta repo that can be assigned and graded."""

    path = models.CharField(max_length=100, primary_key=True)
    # when the assignment will be collected
    due_date = models.DateTimeField(null=True)


class Submission(models.Model):
    """Commit for a Student that was on 'master' at the time of an Assignment due date."""

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    commit = models.ForeignKey(Commit, on_delete=models.CASCADE)
