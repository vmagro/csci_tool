import errno
import logging
from os import path
import sys

from ..repo import Repo
from ..student import Student


logger = logging.getLogger(__name__)


class BaseCommand(object):
    """Superclass for all subcommands in csci_tool
    Provides some conveniences to read arguments from the user interactively or
    from the command line.
    """

    def add_argument(self, *args, **kwargs):
        """Wrapper around ArgumentParser.add_argument that saves some
        information to enable intelligent prompting."""
        # look in the args list for flags/names
        names = [arg for arg in args[:2] if isinstance(arg, str)]
        # remove leading '-' or '--'
        names = [name.lstrip('-') for name in names]
        help_str = kwargs['help'] if 'help' in kwargs else None
        try:
            self.args.append((names, help_str))
        except AttributeError:
            # if we haven't created any args yet make the list now
            self.args = [(names, help_str)]

        # add it to the real parser
        self.parser.add_argument(*args, **kwargs)

    def populate_parser(self, subparsers):
        """Populate an subparser with the options for this subcommand"""
        self.parser = subparsers.add_parser(self.NAME, help=self.HELP)
        self.parser.set_defaults(command=self)
        self.populate_args()

    def populate_args(self):
        """Populate the subparser with arguments by calling self.add_argument"""
        pass

    def run(self, args):
        """Run with the args from the subparser"""
        raise NotImplementedError('Subcommands must implement run')

    def prompt(self, args, key):
        """Intelligently prompt the user for some data, first checking if it's
        already present in the arguments.
        """
        # find the help for the given argument, default to just the name
        help = key
        if hasattr(self, 'args'):
            for opt in self.args:
                names = opt[0]
                help_str = opt[1]
                if key in names:
                    help = help_str

        if hasattr(args, key) and getattr(args, key) is not None:
            return getattr(args, key)
        else:
            return input('{}: '.format(help))

    def load_students(self, students_file=None):
        """Load student info from an input stream or defaulting to students.txt
        in meta repo

        Returns:
            list of Student
        """
        # load student info from meta repo text file
        try:
            # allow passing students file in as an argument to only mutate
            # certain repos - default to the meta repo students.txt
            if students_file == sys.stdin:
                print('Please enter students emails and GitHub names one per ' +
                      'line separated by a space')
                print('Repos will be collected after EOF\n')
            if students_file is None:
                meta_dir = Repo.meta_repo().working_tree_dir
                students_file = open(path.join(meta_dir, 'students.txt'), 'r')

            students = students_file.readlines()
            students = [s.strip() for s in students]
            students = [s for s in students if s]  # filter out empty lines
            students = [s.split(' ') for s in students]
            students = [Student(email=s[0], github=s[1]) for s in students]
        except OSError as e:
            if e.errno == errno.ENOENT:
                logger.warning('No students.txt found, no changes will be made')
            raise
        return students
