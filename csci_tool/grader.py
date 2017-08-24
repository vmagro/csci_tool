import importlib.util
import logging
import os

from .repo import Repo

logger = logging.getLogger(__name__)


class Grader():
    """Grader is an interface to grade assignments in student github repos.

    A Grader is run for every student's repo when the admin runs an grading
    command from the cli. Graders have two functions, automatic grading and
    human grading.
    In automatic mode, the Grader returns a tuple (score, max_score).
    In human mode, the Grader returns a list of files that should be shown to
    the user interactively.

    Graders may be run in parallel so must be thread-safe.

    Graders should live in a subdirectory of the template repo and be named
    'grader.py' which will automatically be run by the CLI.

    Graders must implement two functions as described below:
        auto_grade(student, source_dir):
            auto_grade gives a student submission an automatic score

            Arguments:
                student (Student)
                source_dir (PathLike): directory where grade.py lives
            Returns:
                tuple (list, int): (list_of_scores, max_score)

        human_grade(student, source_dir):
            Arguments:
                student (Student)
                source_dir (PathLike): directory where grade.py lives
            Returns:
                list of str: files that should be shown to the grader

        auto_grade and human_grade are run with cwd set to the corresponding
        directory in the student repo, for example for
        <template>/datalab/grader.py, os.getcwd() will return <student>/datalab/
    """

    @staticmethod
    def get_grader(name):
        """Loads a Grader from the template repo by name (AKA subdirectory)

        Arguments:
            name (str): name of grader (subdir it lives in)
        Returns:
            module with functions auto_grade and human_grade
        """
        meta_dir = Repo.meta_repo().working_tree_dir
        py_path = os.path.join(meta_dir, name, 'grade.py')
        logger.info('Loading grader from %s', py_path)
        spec = importlib.util.spec_from_file_location(name + '.grade', py_path)
        grader = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(grader)
        logger.info('Imported %s', py_path)
        return grader
