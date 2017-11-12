import argparse
import logging
import os
from os import path
import tempfile
import git
from distutils import dir_util

from .base import BaseCommand
from ..config import Config
from ..student import Student


logger = logging.getLogger(__name__)


class CollectLateCommand(BaseCommand):
    NAME = 'collect-late'
    HELP = 'collect student repos as submodules for an assignment, using specific SHAs'

    def populate_args(self):
        self.add_argument('assignment', help='assignment name')
        self.add_argument('submissions', help='submissions file', nargs='?',
                          type=argparse.FileType('r'),
                          default=None)
        self.add_argument('destination', help='dest directory')

    def run(self, args):
        assignment = args.assignment
        logger.info('Collecting late submissions for %s', assignment)

        config = Config.load_config()
        github = config.github

        failures = []

        for line in args.submissions:
            email, late_days, sha = line.strip().split(',')
            logger.info('Collecting %s from %s for %s, %s late day(s)',
                        sha, email, assignment, late_days)
            try:
                student = Student(email, None)

                # clone the repo into the subdirectory at args.destination
                dest_dir = path.join(args.destination, student.unix_name)
                # just add a submodule rather than downloading the whole repo
                with tempfile.TemporaryDirectory() as tmpdir:
                    # clone the repo into a temp directory and copy the assignment dir to the submissions dir
                    repo = git.Repo.clone_from(student.repo_url, tmpdir)

                    # make sure we got the right sha
                    repo.git.checkout(sha)

                    dir_util.copy_tree(path.join(tmpdir, assignment), dest_dir)

                # comment on the commit that we collected
                repo_fqn = config.github_org + '/' + student.repo_name
                # must use fully qualified repo name with org
                repo = github.get_repo(repo_fqn)
                commit = repo.get_commits(sha=sha)[0]

                comment = 'This commit was collected as part of "{}". \n \
This was a late submission using {} late day(s). If you think this is \
incorrect, please post on Piazza.'.format(assignment, late_days)
                logger.debug('Commenting on GitHub')
                commit.create_comment(comment)
            except Exception as e:
                logger.error('Failed for %s, %s', email, e)
                failures.append((email, late_days, sha))

        if failures:
            logger.error('Failed on %d students, please try them again', len(failures))
            logger.error('Failures have been written out to ./failures.txt')
            with open('failures.txt', 'w') as f:
                for s in failures:
                    f.write('{},{},{}\n'.format(email, late_days, sha))
