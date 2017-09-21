"""Commands for interacting with student data."""

from .base import BaseCommand

from ..models import Student


class StudentCommand(BaseCommand):

    NAME = 'students'
    HELP = 'interact with student data'

    def populate_args(self):
        self.add_argument('command', choices=('list', 'get', 'create', 'delete'))

    def run(self, api, args):
        if args.command == 'list':
            students = api.students.list()
            for s in students:
                s = Student(s)
                print(s)
