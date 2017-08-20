from collections import namedtuple
import importlib.util
import logging
import os

from .repo import Repo

Mutation = namedtuple('Mutation', 'commit_message')

logger = logging.getLogger(__name__)


class Mutator():
    """Mutator is an interface to make modifications to student github repos.
    Mutators are responsible for modifying the working copy of a
    student repo - for example to create the starter files for an assignment.

    A Mutator is run for every student's repo when the admin runs an update from
    the cli. Mutators may be run in parallel so must be thread-safe.

    Mutators should live in a subdirectory of the template repo and be named
    'mutate.py' which will automatically be run by the CLI.

    Mutators must implement a function mute as described below:
        mutate changes the working copy of a student repo
        There is no need to commit the changes, the mutation runner will run the
        mutator, then commit the changes.
        mutate is run with cwd set to the corresponding directory in the student
        repo, for example for <template>/datalab/mutate.py, os.getcwd will be
        <student>/datalab/

        Arguments:
            student (Student)
            source_dir (PathLike): directory where mutate.py lives
        Returns:
            Mutation: metadata about what was changed
    """

    @staticmethod
    def get_mutator(name):
        """Loads a Mutator from the template repo by name (AKA subdirectory)

        Arguments:
            name (str): name of mutator (subdir it lives in)
        Returns:
            function: mutator loaded from mutate.py (function named mutate)
        """
        template_dir = Repo.meta_repo().working_tree_dir
        py_path = os.path.join(template_dir, name, 'mutate.py')
        logger.info('Loading mutator from %s', py_path)
        spec = importlib.util.spec_from_file_location(name + '.mutate', py_path)
        mutate = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mutate)
        logger.info('Imported %s', py_path)
        return mutate.mutate
