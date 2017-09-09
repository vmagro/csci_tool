import argparse
import logging
from os import path

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
            except:
                logger.error('Failed to collect %s', student.unix_name)
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
