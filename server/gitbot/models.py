"""Database models supporting the gitbot application."""

from django.db import models
from django.core.validators import validate_comma_separated_integer_list

from .app_settings import GITHUB_ORG


class Course(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        """Return human-readable representation."""
        return 'Course: {}'.format(self.name)


class CourseSetting(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    key = models.CharField(max_length=200)
    value = models.CharField(max_length=200)

    class Meta:
        """A setting key must be unique in a course."""

        unique_together = ('course', 'key')

    @classmethod
    def get_setting(cls, course, key):
        return cls.objects.get(course=course, key=key)

    def __str__(self):
        """Return human-readable representation."""
        return 'Setting for {} - {}: {}'.format(self.course.name, self.key, self.value)


class Student(models.Model):
    """A Student with a repo that we will give/collect assignments to/from."""

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    usc_email = models.EmailField()
    usc_id = models.CharField(max_length=20)
    github_username = models.CharField(max_length=100)
    preferred_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    # is this student in the canary list (which probably means they're really a CP)
    # this is used to more safely test new versions of mutations or grading scripts as we can run on
    # only repos that are marked as canaries
    canary = models.BooleanField(default=False)

    class Meta:
        """Provide stronger uniqueness guarantees."""
        # there can only be one student with a given email, id or github in a course
        unique_together = (('course', 'usc_email'), ('course', 'usc_id'),
                           ('course', 'github_username'))

    @property
    def unix_name(self):
        """USC username extraced from email."""
        return self.usc_email[:-len('@usc.edu')]

    def __str__(self):
        """Return human-readable representation."""
        return 'Student: {} {} {}'.format(self.unix_name, self.first_name, self.last_name)


class Repo(models.Model):
    """A Student GitHub repo."""

    student = models.OneToOneField(Student, primary_key=True, on_delete=models.CASCADE)
    # full repo name eg: (vmagro/csci_tool)
    name = models.CharField(max_length=200)

    @property
    def short_name(self):
        """Get the repo's short name by removing the leading organization name."""
        return self.name[self.name.index() + 1:]

    @property
    def repo_url(self):
        """Cloneable URL to a REPO."""
        return 'git@github.com:{}.git'.format(self.name)

    def head_commit(self):
        """Get whatever the latest commit is to this repo at the current point in time."""
        return self.commit_set.order_by('-commit_date').first()

    def __str__(self):
        """Return human-readable representation."""
        return 'Repo: {} for {}'.format(self.name, self.student)


class Commit(models.Model):
    """Commit that is either a user commit or a bot commit."""

    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
    sha = models.CharField(max_length=200, primary_key=True)
    author = models.CharField(max_length=100)
    commit_date = models.DateTimeField()
    push_date = models.DateTimeField()
    message = models.CharField(max_length=200)

    class Meta:
        """Provide stronger uniqueness guarantees."""

        unique_together = ('repo', 'sha')


class Assignment(models.Model):
    """An Assignment is a directory in the meta repo that can be assigned and graded."""

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    path = models.CharField(max_length=100, editable=False)
    # when the assignment will be collected
    due_date = models.DateTimeField(null=True, editable=False)

    # human-readable status message about this assignment
    status = models.CharField(max_length=200)

    class Meta:
        """There can only be one assignment model for each path in one course."""

        unique_together = ('course', 'path')

    @property
    def name(self):
        """Someday we may want a customizable name for an assignment, but just use path for now."""
        return self.path

    def __str__(self):
        """Return human-readable representation."""
        return 'Assignment: {}, due {}'.format(self.path, self.due_date)


class Submission(models.Model):
    """Commit for a Student that was on 'master' at the time of an Assignment due date."""

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    commit = models.ForeignKey(Commit, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    late_days_used = models.IntegerField(default=0)

    # store a "list" of grades as comma separated integers
    grades = models.CharField(max_length=100, default='',
                              validators=[validate_comma_separated_integer_list])

    class Meta:
        """Provide stronger uniqueness guarantees."""

        unique_together = ('student', 'assignment', 'commit')


class Mutation(models.Model):
    """Changes the bot made to a repo and for what assignment."""

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    sha = models.CharField(max_length=200, primary_key=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
