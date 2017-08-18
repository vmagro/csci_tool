import logging

from .base import BaseCommand
from ..config import Config
from ..repo import Repo
from ..student import Student

logger = logging.getLogger(__name__)


class MutateCommand(BaseCommand):
    NAME = 'mutate'
    HELP = 'update student repos'
    OPTIONS = [
        ('-m', '--mutation', 'name of mutator (directory it lives in)'),
    ]

    def run(self, args):
        mutation = self.prompt(args, 'mutation')

        # make sure that the requested mutation actully exists

        config = Config.load_config()

        # TODO(vmagro): load students from a file in the meta repo
        students = [
            Student(email='smagro@usc.edu', github='vmagro'),
        ]
        logger.info('Loaded %d students', len(students))

        # clone all the repos first
        def clone(student):
            path = Repo.clone_student_repo(student)
            return student, path
        repos = [clone(s) for s in students]

        for student, repo_path in repos:
            logger.info('Mutating repo: %s', student.github)
            pass
