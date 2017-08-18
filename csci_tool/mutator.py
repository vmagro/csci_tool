from abc import ABCMeta, abstractmethod
from collections import namedtuple

Mutation = namedtuple('Mutation', 'commit_message')


class Mutator(metaclass=ABCMeta):
    """Mutator is an interface to make modifications to student github repos.
    Mutators are responsible for modifying the working copy of a
    student repo - for example to create the starter files for an assignment.

    A Mutator is run for every student's repo when the admin runs an update from
    the cli. Mutators may be run in parallel so must be thread-safe.

    Mutators should live in a subdirectory of the template repo and be named
    'mutate.py' which will automatically be run by the CLI.
    """

    @abstractmethod
    def mutate(self, student):
        """mutate changes the working copy of a student repo
        There is no need to commit the changes, the mutation runner will run the
        mutator, then commit the changes.
        mutate is run with cwd set to the corresponding directory in the student
        repo, for example for <template>/datalab/mutate.py, os.getcwd will be
        <student>/datalab/

        Args:
            student (Student)
        Returns:
            Mutation: metadata about what was changed
        """
        raise NotImplementedError('Must be implemented by a subclass')
