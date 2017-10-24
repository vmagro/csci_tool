"""Load course settings from config file."""

import yaml


class CourseSettings(object):
    """Settings for a course."""

    __slots__ = ('course', 'settings')

    @classmethod
    def get_settings():
        """Load from the default path (current directory)."""
        return CourseSettings(open('./settings.yml', 'r'))

    def __init__(self, input):
        """Load settings from an input file or string."""
        self.settings = yaml.load(input)['settings']

    def __getitem__(self, key):
        """Allow subscript notation to access settings."""
        return self.get(key)

    # this allows us to do something like settings.github_org to get the github_org setting
    def __getattr__(self, key):
        """Allow dot notation to access settings."""
        return self.get(key)

    def get(self, key, default=None):
        """Allow dict-style .get to access settings."""
        val = self.settings.get(key, default)
        if val == 'True':
            return True
        elif val == 'False':
            return False
        return val
