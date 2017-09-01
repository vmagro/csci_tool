import errno
from git import Repo as GitRepo
import logging
import os
from os import path
import sys

from .base import BaseCommand
from ..config import Config

logger = logging.getLogger(__name__)


class LoginCommand(BaseCommand):
    NAME = 'login'
    HELP = 'login to admin a course'

    def populate_args(self):
        self.add_argument('-g', '--github', help='GitHub username')
        self.add_argument('-e', '--email', help='USC email')
        self.add_argument('-p', '--password', help='GitHub password (or personal access token)')  # noqa
        self.add_argument('-o', '--org', help='GitHub org')
        self.add_argument('-m', '--meta', help='Meta repo name', default='meta')

    def run(self, args):
        github = self.prompt(args, 'github')
        email = self.prompt(args, 'email')
        github_password = self.prompt(args, 'password')
        org = self.prompt(args, 'org')
        meta_name = self.prompt(args, 'meta')
        if not email.endswith('@usc.edu'):
            print('You must use your USC email address')
            sys.exit(1)

        # save the user information to the config file
        # save into ~/.csci/cscirc by default
        try:
            os.mkdir(path.join(path.expanduser('~'), '.csci'))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        config_path = path.join(path.expanduser('~'), '.csci', 'cscirc')

        config = Config(config_path)
        config.github_login = github
        config.email = email
        config.github_org = org
        config.meta_name = meta_name
        config.github = github_password

        logger.debug('Writing config to %s', config_path)
        config.save()

        logger.info('Cloning meta repo into %s', config.meta_path)
        GitRepo.clone_from(config.meta_remote, config.meta_path)
        logger.info('Cloned meta repo')
