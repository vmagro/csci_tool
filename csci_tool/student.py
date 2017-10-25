from .course_settings import CourseSettings


class Student(object):

    def __init__(self, usc_email, usc_id, preferred_name, first_name, last_name, github_userame):
        self.usc_email = usc_email
        self.usc_id = usc_id
        self.preferred_name = preferred_name
        self.first_name = first_name
        self.last_name = last_name
        self.github_username = github_userame

    @property
    def repo_name(self):
        """Get a string name for the student's repo."""
        return CourseSettings.get_settings().student_repo_format.format(**self.__dict__).lower()

    @property
    def repo_url(self):
        """Get a cloneable URL to the student's GitHub repo."""
        settings = CourseSettings.get_settings()
        return f'https://{settings.bot_username}:{settings.bot_token}@github.com/{settings.github_org}/{self.repo_name}.git'

    def __str__(self):
        return f'{self.preferred_name} {self.last_name} <{self.usc_email}>'
