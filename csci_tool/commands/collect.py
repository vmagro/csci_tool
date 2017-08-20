import argparse
import logging
from os import path

from .base import BaseCommand
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
        logger.info('Collecting from %d students', len(students))

        meta_repo = Repo.meta_repo()

        for student in students:
            dest_dir = path.join('submissions', assignment, student.unix_name)
            # just add a submodule rather than downloading the whole repo
            sub = meta_repo.create_submodule(
                name='{}_{}'.format(assignment, student.unix_name),
                path=dest_dir,
                url=student.repo_url
            )

            logger.info('Collected %s at %s into %s', student.unix_name,
                        sub.hexsha, dest_dir)

        meta_repo.index.commit('Collecting {} from {} students'
                               .format(assignment, len(students)))
        meta_repo.remote().push()
