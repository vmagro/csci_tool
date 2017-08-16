import errno
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
    HELP = 'setup a new repository'
    OPTIONS = [
        ('-g', '--github', 'GitHub username'),
        ('-e', '--email', 'USC email'),
        # TODO(vmagro) make generic for different classes
        # ('-c', '--course', 'CSCI course number (eg 356)'),
    ]

    def run(self, args):
        github = self.prompt(args, 'github')
        email = self.prompt(args, 'email')
        if not email.endswith('@usc.edu'):
            print('You must use your USC email address')
            sys.exit(1)
        # TODO(vmagro) make generic for different classes
        # course_number = self.prompt(args, 'course')
        course_number = '356'
        course_name = 'csci' + course_number

        # make a request to the server to invite them to the org
        print('Check your email for an invitation to our GitHub organization')
        print('This process will stay running until you accept the invitation')
        print('If there are any issues, you can re-run \'csci init --resume\' '
              'from this directory')

        logger.info('Checking if GitHub repo has been created yet')
        # now request on an interval to wait for them to accept so we can
        # initialize their repo
        project_name = 'csci' + course_number
        project_path = path.join(os.getcwd(), project_name)
        logger.info('Creating %s for repo', project_path)
        try:
            os.mkdir(project_path)
        except OSError as e:
            # swallow EEXIST, raise all others
            if e.errno != errno.EEXIST:
                raise

        # save the user information to the config file
        config_path = path.join(project_path, '.cscirc')

        config = Config(config_path)
        config.github = github
        config.email = email

        logger.debug('Writing config to %s', config_path)
        config.save()

        # repo exists, lets fill it with some data
        repo = Repo(project_path)
        repo.init_student_repo(Repo.get_template_repo(course_name), config)
