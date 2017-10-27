"""Repo utils to work with a repo's files locally."""

from distutils import dir_util
import logging
import subprocess
import tempfile
from typing import Type

from .models import Student

logger = logging.getLogger(__name__)


class LocalRepo(object):
    """A LocalRepo is a copy of a student repo stored on disk."""

    path: str

    def __init__(self, path: str):
        """Init a LocalRepo at a specific path."""
        self.path = path

    @staticmethod
    def clone_from_url(url: str, path: str):
        """Clone a repo to local disk given a git url."""
        logger.debug('Repo path: %s', path)
        instance = LocalRepo(path)
        subprocess.run(['git', 'clone', '--depth', '1', url, instance.path], check=True)
        return instance

    @staticmethod
    def clone_repo(student: Type[Student]):
        """Clone a repo to local disk given information from the database."""
        logger.info('Cloning repo for %s', student.unix_name)
        path = tempfile.mkdtemp(prefix='gitbot', suffix=student.unix_name)
        return LocalRepo.clone_from_url(student.repo_url, path)

    def run(self, cmd, **kwargs):
        """Run the command list through subprocess in the repo working directory."""
        try:
            return subprocess.run(cmd, check=True, cwd=self.path,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)
        except subprocess.CalledProcessError as e:
            logger.error('Subprocess failed')
            logger.error('stdout:')
            logger.error(e.stdout)
            logger.error('stderr:')
            logger.error(e.stderr)
            raise

    def commit(self, author_name: str, author_email: str, commit_message: str):
        """Make a commit in the repo using the given author and message."""
        # first add all the things
        self.run(['git', 'add', '.'])
        # then make the commit
        self.run(['git', 'commit',
                  '--author="{} <{}>"'.format(author_name, author_email),
                  '-m', commit_message,
                  '--allow-empty',  # a lot of time we want to make an empty commit during testing
                  ])
        # just for fun return the sha of the commit we just made
        return self.run(['git', 'rev-parse', 'head']).stdout.decode('utf-8')

    def push(self):
        """Push local commit(s) to GitHub."""
        self.run(['git', 'push'])

    def pull(self):
        """Pull remote changes from GitHub."""
        self.run(['git', 'pull'])

    def delete(self):
        """Delete the temporary directory."""
        logger.info('Deleting repo at %s', self.path)
        dir_util.remove_tree(self.path)
