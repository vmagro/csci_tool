import argparse
import logging
import os
from os import path
import datetime
import tempfile
import git
from distutils import dir_util

from .base import BaseCommand
from ..config import Config
from ..repo import Repo


logger = logging.getLogger(__name__)


class CollectCommand(BaseCommand):
    NAME = 'collect'
    HELP = 'collect student repos as submodules for an assignment'

    def populate_args(self):
        self.add_argument('assignment', help='assignment name')
        self.add_argument('students', help='students file', nargs='?',
                          type=argparse.FileType('r'),
                          default=None)
        self.add_argument('destination', help='dest directory')
        self.add_argument('deadline', help='deadline in the form of "2017-11-07 00:05:00 -0700"', nargs='?', default=None)

    def run(self, args):
        assignment = args.assignment
        students = self.load_students(args.students)
        logger.info('Collecting %s from %d students', assignment, len(students))

        os.makedirs(args.destination, exist_ok=True)

        meta_repo = Repo.meta_repo()
        config = Config.load_config()
        github = config.github

        failures = []
        for student in students:
            try:
                # clone the repo into the subdirectory at args.destination
                dest_dir = path.join(args.destination, student.unix_name)
                # just add a submodule rather than downloading the whole repo
                with tempfile.TemporaryDirectory() as tmpdir:
                    # clone the repo into a temp directory and copy the assignment dir to the submissions dir
                    repo = git.Repo.clone_from(student.repo_url, tmpdir)

                    # if we have a deadline check out the commit from master at that time
                    if args.deadline is not None:
                        rev_list = getattr(repo.git, 'rev-list')
                        sha = rev_list('master', n=1, before=args.deadline)
                        dir_util.copy_tree(path.join(tmpdir, assignment), dest_dir)
                    else:
                        sha = repo.head.commit.hexsha

                logger.info('Collected %s at %s into %s', student.unix_name,
                            sha, dest_dir)

                # comment on the commit that we collected
                repo_fqn = config.github_org + '/' + student.repo_name
                # must use fully qualified repo name with org
                repo = github.get_repo(repo_fqn)
                commit = repo.get_commits(sha=sha)[0]
                comment = 'This commit was collected as part of "{}". \n \
If you think this was a mistake or you want to submit this assignment late, \
please fill out the late form.'.format(assignment)
                commit.create_comment(comment)
            except Exception as e:
                logger.error('Failed to collect %s', student.unix_name)
                logger.error(e)
                failures.append(student)

        if failures:
            logger.error('Failed on %d students, please try them again', len(failures))
            logger.error('Failures have been written out to ./failures.txt')
            with open('failures.txt', 'w') as f:
                for s in failures:
                    f.write(s.email + ' ' + s.github + '\n')

        # commit all the submissions at once

        meta_repo.index.commit('Collected {} from {} students'
                               .format(assignment, len(students)))
        meta_repo.remote().push()
