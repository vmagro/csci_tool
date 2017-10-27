from .course_settings import CourseSettings

from . import orm
from .orm import Model


class Student(Model):

    usc_email = orm.Field()
    usc_id = orm.Field()
    preferred_name = orm.Field()
    first_name = orm.Field()
    last_name = orm.Field()
    github_username = orm.Field()

    @property
    def repo_name(self):
        """Get a string name for the student's repo."""
        return CourseSettings.get_settings().student_repo_format.format(**self.__dict__).lower()

    @property
    def repo_url(self):
        """Get a cloneable URL to the student's GitHub repo."""
        settings = CourseSettings.get_settings()
        return 'https://{}:{}@github.com/{}/{}.git'.format(
            settings.bot_username, settings.bot_token, settings.github_org, self.repo_name
        )
