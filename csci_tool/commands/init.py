import errno
from git import Repo as GitRepo
import logging
import os
from os import path
import sys

from .base import BaseCommand
from ..config import Config
from ..repo import Repo

logger = logging.getLogger(__name__)


class InitCommand(BaseCommand):
    NAME = 'init'
    HELP = 'login to admin a course'

    def populate_args(self):
        self.add_argument('-g', '--github', help='GitHub username')
        self.add_argument('-e', '--email', help='USC email')

    def run(self, args):
        github = self.prompt(args, 'github')
        email = self.prompt(args, 'email')
        if not email.endswith('@usc.edu'):
            print('You must use your USC email address')
            sys.exit(1)
        # TODO(vmagro) make generic for different classes
        # course_number = self.prompt(args, 'course')

        # save the user information to the config file
        # save into ~/.csci/.cscirc by default
        try:
            os.mkdir(path.join(path.expanduser('~'), '.csci'))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        config_path = path.join(path.expanduser('~'), '.csci', '.cscirc')

        config = Config(config_path)
        config.github = github
        config.email = email
        # TODO(vmagro) make generic for different classes
        config.meta_name = 'meta'
        config.github_org = 'usc_csci356_fall17'

        logger.debug('Writing config to %s', config_path)
        config.save()

        logger.info('Cloning meta repo into %s', config.meta_path)
        GitRepo.clone_from(config.meta_remote, config.meta_path)
        logger.info('Cloned meta repo')
