"""Repo utils to work with a repo's files locally."""

from distutils import dir_util
import logging
import subprocess
from tempfile import TemporaryDirectory
from typing import Type

from .app_settings import BOT_PRIVATE_KEY_PATH as private_key_path
from .models import Student, Repo as DBRepo


logger = logging.getLogger(__name__)


class LocalRepo(object):
    """A LocalRepo is a copy of a student repo stored on disk."""

    path: str
    student: Type[Student]

    @staticmethod
    def clone_repo(repo_stub: Type[DBRepo]):
        """Clone a repo to local disk given information from the database."""
        logger.info('Cloning repo for %s', repo_stub.student.unix_name)
        instance = LocalRepo()
        path = TemporaryDirectory(prefix='gitbot', suffix=repo_stub.student.unix_name)
        logger.debugh('Repo path: %s', path)
        instance.path = path
        subprocess.run(['git', 'clone', '--depth', '1', repo_stub.repo_url, instance.path])
        return instance

    def run(self, cmd, **kwargs):
        """Run the command list through subprocess in the repo working directory."""
        # if they're using a private key path, set it up so that git will use it
        env = {}
        if private_key_path:
            env['GIT_SSH_COMMAND'] = 'ssh -i {}'.format(private_key_path)

        return subprocess.run(cmd, check=True, cwd=self.path, env=env,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)

    def commit(self, author_name: str, author_email: str, commit_message: str):
        """Make a commit in the repo using the given author and message."""
        # first add all the things
        self.run(['git', 'add', '.'])
        # then make the commit
        self.run(['git', 'commit',
                  '--author="{} <{}>"'.format(author_name, author_email),
                  '-m', commit_message])
        # just for fun return the sha of the commit we just made
        return self.run(['git', 'rev-parse', 'head']).stdout.decode('utf-8')

    def push(self):
        """Push local commit(s) to GitHub."""
        self.run(['git', 'push'])

    def delete(self):
        """Delete the temporary directory."""
        logger.info('Deleting repo at %s', self.path)
        dir_util.remove_tree(self.path)
