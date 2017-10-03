import argparse
import logging
from os import path
import datetime

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
        self.add_argument('deadline', help='deadline as a unix epoch', default=None)

    def run(self, args):
        assignment = args.assignment
        students = self.load_students(args.students)
        logger.info('Collecting %s from %d students', assignment, len(students))

        meta_repo = Repo.meta_repo()
        config = Config.load_config()
        github = config.github

        failures = []
        for student in students:
            try:
                dest_dir = path.join('submissions', assignment, student.unix_name)
                # just add a submodule rather than downloading the whole repo
                sub = meta_repo.create_submodule(
                    name='{}_{}'.format(assignment, student.unix_name),
                    path=dest_dir,
                    url=student.repo_url
                )
                # if we were given a deadline, update the submodule to the specific commit
                if args.deadline is not None:
                    # get the latest commit before the deadline
                    deadline = datetime.datetime.fromtimestamp(int(args.deadline))
                    sha = None
                    repo_fqn = config.github_org + '/' + student.repo_name
                    # must use fully qualified repo name with org
                    repo = github.get_repo(repo_fqn)
                    for c in repo.get_commits():
                        if c.commit.author.date <= deadline:
                            sha = c.sha
                            break
                    sub.module().git.checkout(sha)
                    logger.debug('Adding to index')
                    # this magic incantation is required to get GitPython to commit
                    sub.binsha = sub.module().head.commit.binsha
                    meta_repo.index.add([sub])

                logger.info('Collected %s at %s into %s', student.unix_name,
                            sub.hexsha, dest_dir)

                # comment on the commit that we collected
                repo_fqn = config.github_org + '/' + student.repo_name
                # must use fully qualified repo name with org
                repo = github.get_repo(repo_fqn)
                commit = repo.get_commits(sha=sub.hexsha)[0]
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
