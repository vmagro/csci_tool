"""
Configuration loader
Loads an INI config file (.cscirc) to determine application settings, starting
by looking in the current directory, then up a level recursively until found or
@staticmethod
def load_config(path):

reaches '/', then looks in the user's homedir
"""

from configparser import ConfigParser
import errno
import logging
import os
from os import path


logger = logging.getLogger(__name__)
logger.setLevel(30)  # config logs are really noisy


class Config(object):
    """.cscirc formatter

    Attributes:
        path (PathLike): path to config file
        github (str): github account name
        email (str): USC email address
        course (str): course number (eg '356')
    """

    def __init__(self, path=None, config_parser=None):
        self.path = path
        if config_parser is not None:
            self._config = config_parser
        else:
            self._config = ConfigParser()

    @staticmethod
    def load_config(path=None):
        """Uses ConfigParser to load config from .cscirc, using the search algorithm
        from find_config to find the relevant file.
        """
        f = path if path is not None else None
        if f is None:
            f = Config.find_config(os.getcwd())
        if f is None:
            raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), '.cscirc')
        config = ConfigParser()
        config.read(f)
        return Config(f, config)

    @staticmethod
    def find_config(d):
        """Find the .cscirc config file relevant to this project
        This recurses up to parent directories until reaching /, returning the
        first .cscirc found, or ~/.cscirc

        Arguments:
            d (str): directory to start searching (usually cwd)
        Returns:
            PathLike path to config file to use
        """
        logger.debug('Checking for %s/.cscirc', d)
        if path.isfile(path.join(d, '.cscirc')):
            logger.debug('Found .cscirc in %s', d)
            return path.join(d, '.cscirc')
        elif path.dirname(d) == d:
            # don't go up past /
            # default to ~/.csci/.cscirc
            logger.debug('Defaulting to config ~/.csci/cscirc')
            return path.join(path.expanduser('~'), '.csci', 'cscirc')
        else:
            parent = path.dirname(d)
            logger.debug('Didn\'t find .cscirc in %s, checking %s', d, parent)
            return Config.find_config(parent)

    def save(self, path=None):
        """Write the current config to the config file"""
        if path is None:
            path = self.path
        with open(path, 'w+') as config_file:
            self._config.write(config_file)

    @property
    def github(self):
        return self._config['user']['github']

    @github.setter
    def github(self, github):
        if 'user' not in self._config:
            self._config['user'] = {}
        self._config['user']['github'] = github

    @property
    def email(self):
        return self._config['user']['email']

    @email.setter
    def email(self, email):
        if 'user' not in self._config:
            self._config['user'] = {}
        self._config['user']['email'] = email

    @property
    def unix_name(self):
        """USC Unix name AKA prefix of email"""
        return self.email[:-len('@usc.edu')]

    @property
    def meta_name(self):
        """Name for meta git repo (in the GitHub organization)"""
        return self._config['repo']['meta_name']

    @meta_name.setter
    def meta_name(self, name):
        if 'repo' not in self._config:
            self._config['repo'] = {}
        self._config['repo']['meta_name'] = name

    @property
    def meta_path(self):
        """Path to meta git repo"""
        # lives in a subdirectory next to .cscirc
        dir_name = self.github_org + '_' + self.meta_name
        return path.join(path.dirname(self.path), dir_name)

    @property
    def meta_remote(self):
        """Git remote URL to meta repo"""
        return 'ssh://git@github.com/' + \
            self.github_org + '/' + self.meta_name + '.git'

    @property
    def github_org(self):
        """Name of github org (eg ctcusc for github.com/ctcusc"""
        return self._config['repo']['github_org']

    @github_org.setter
    def github_org(self, org):
        if 'repo' not in self._config:
            self._config['repo'] = {}
        self._config['repo']['github_org'] = org
