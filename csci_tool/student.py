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
        repo_name = 'hw_' + self.unix_name
        config = Config.load_config()
        return 'ssh://git@github.com:' + \
            config.github_org + '/' + repo_name + '.git'

    @property
    def unix_name(self):
        """USC Unix name AKA prefix of email"""
        return self.email[:-len('@usc.edu')]

    def __str(self):
        return self.github + ' <' + self.email + '>'
