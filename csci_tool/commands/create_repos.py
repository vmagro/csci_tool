import argparse
import errno
import logging
import os
from os import path
import sys

from .base import BaseCommand
from ..config import Config
from ..repo import Repo
from ..student import Student

logger = logging.getLogger(__name__)


class CreateReposCommand(BaseCommand):
    NAME = 'create-repos'
    HELP = 'create student repos'

    def populate_args(self):
        self.add_argument('students', nargs='?', type=argparse.FileType('r'),
                          default=sys.stdin)

    def run(self, args):
        if args.students == sys.stdin:
            if sys.stdout.isatty():
                print('Please enter students emails and GitHub names one per ' +
                      'line separated by a space')
                print('Repos will be created after EOF\n')

        students = args.students.readlines()
        students = [s.strip() for s in students]
        students = [s for s in students if s]  # filter out empty lines
        students = [s.split(' ') for s in students]
        students = [Student(email=s[0], github=s[1]) for s in students]

        # deduplicate based on existing students.txt
        config = Config.load_config()
        meta_repo = Repo.meta_repo()
        meta_dir = meta_repo.working_tree_dir

        try:
            with open(path.join(meta_dir, 'students.txt'), 'r') as f:
                existing = f.readlines()
                existing = [e.strip().split(' ') for e in existing]
                existing = [Student(email=s[0], github=s[1]) for s in existing]
                existing = {s.email for s in existing}

                # now dedup based on the existing set
                orig = len(students)
                students = [s for s in students if s.email not in existing]
                logger.debug('Removed %d students already present',
                             orig - len(students))
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

        # now that we've deduplicated, make any changes
        if len(students) == 0:
            print('No student data found, not creating repos')
            return

        logger.info('Creating repos for %d students', len(students))

        github = config.github
        org = github.get_organization(config.github_org)

        for student in students:
            # call github api to create student repo
            logger.info('Creating repo %s', student.repo_name)
            repo = org.create_repo(student.repo_name,
                                   'Homework for {}'.format(student.email),
                                   # private=True,
                                  )
            logger.info('Adding %s to collaborators', student.github)
            repo.add_to_collaborators(student.github)

        # make a commit with the new students in the meta repo
        cwd = os.getcwd()
        os.chdir(config.meta_path)

        with open('students.txt', 'a') as github_file:
            lines = [s.email + ' ' + s.github + '\n' for s in students]
            github_file.writelines(lines)

        logger.debug('Adding students.txt to index')
        meta_repo.index.add(['students.txt'])
        logger.debug('Commiting changes')
        meta_repo.index.commit('Added {} students'.format(len(students)))
        logger.debug('Pushing to remote')
        meta_repo.remote().push()

        os.chdir(cwd)

        logger.info('Created repos, pushed updated meta to GitHub')
