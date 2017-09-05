from .config import Config


class Student(object):
    """Store information about a student

    Attributes:
        email (str): USC email address
        github (str): GitHub username
    """

    def __init__(self, email, github):
        assert email.endswith('@usc.edu')
        self.email = email
        self.github = github

    @property
    def repo_url(self):
        """URL to student repo"""
        config = Config.load_config()
        return 'git@github.com:' + \
            config.github_org + '/' + self.repo_name + '.git'

    @property
    def unix_name(self):
        """USC Unix name AKA prefix of email"""
        return self.email[:-len('@usc.edu')]

    @property
    def repo_name(self):
        """Repo name in the organization"""
        return 'hw_' + self.unix_name

    def __str(self):
        return self.github + ' <' + self.email + '>'
