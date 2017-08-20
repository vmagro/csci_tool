import argparse
import errno
from git import Repo as GitRepo
import logging
import os
from os import path

from .base import BaseCommand
from ..mutator import Mutator
from ..repo import Repo
from ..student import Student

l = logging.getLogger(__name__)


class MutateCommand(BaseCommand):
    NAME = 'mutate'
    HELP = 'update student repos'

    def populate_args(self):
        self.add_argument('mutation', help='name of mutator')
        self.add_argument('students', help='students file', nargs='?',
                          type=argparse.FileType('r'),
                          default=None)

    def run(self, args):
        mutation_name = self.prompt(args, 'mutation')

        try:
            mutate = Mutator.get_mutator(mutation_name)
        except AttributeError:
            l.error('mutate.py doesn\'t seem to have a mutate function')
            return
        except:
            l.error('Failed to import mutator "%s", are you sure it exists?',
                    mutation_name)
            return

        meta_dir = Repo.meta_repo().working_tree_dir

        students = self.load_students(args.students)

        l.info('Loaded %d students', len(students))

        # clone all the repos first
        def clone(student):
            try:
                path = Repo.clone_student_repo(student)
            except:
                l.error('Failed to clone repo, does it exist and is your ' +
                        'internet connection working?')
                raise
            return student, path
        try:
            repos = [clone(s) for s in students]
        except:
            l.error('Cloning one or more repos failed')
            return

        # source_dir is where the mutator files exist in the meta repo
        source_dir = path.join(meta_dir, mutation_name)
        # make the changes
        for student, repo_path in repos:
            l.info('Mutating repo: %s', student.unix_name)
            cwd = os.getcwd()
            os.chdir(repo_path)
            os.makedirs(mutation_name, exist_ok=True)
            os.chdir(mutation_name)
            mutate(student, source_dir)
            os.chdir(cwd)

        # commit and push our changes
        for student, repo_path in repos:
            l.info('Committing repo: %s', student.unix_name)
            repo = GitRepo(repo_path)
            repo.index.add('*')
            repo.index.commit('[course staff] ' + mutation_name)
            l.info('Pushing repo: %s', student.unix_name)
            repo.remote().push()
            l.info('Pushed repo: %s', student.unx_name)
