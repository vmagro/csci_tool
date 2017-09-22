"""Commands for interacting with student data."""

from termcolor import colored

from .base import BaseCommand

from ..models import Student


class StudentCommand(BaseCommand):

    NAME = 'students'
    HELP = 'interact with student data'

    def populate_args(self, parser):
        subparsers = parser.add_subparsers()
        subparsers.required = True

        list_students = subparsers.add_parser('list', help='list all students')
        list_students.set_defaults(subcommand=self.list)

        create_student = subparsers.add_parser('create', help='create a student')
        create_student.set_defaults(subcommand=self.create)
        create_student.add_argument('usc_email', help='USC email')
        create_student.add_argument('usc_id', help='USC ID')
        create_student.add_argument('github_username', help='GitHub username')
        create_student.add_argument('preferred_name', help='Preferred Name')
        create_student.add_argument('first_name', help='First Name')
        create_student.add_argument('last_name', help='Last Name')

    def run(self, api, args):
        args.subcommand(api, args)

    def list(self, api, args):
        students = api.students.list()
        for s in students:
            s = Student(s)
            print(s)

    def create(self, api, args):
        student_data = {
            'usc_email': args.usc_email,
            'usc_id': args.usc_id,
            'github_username': args.github_username,
            'preferred_name': args.preferred_name,
            'first_name': args.first_name,
            'last_name': args.last_name,
        }
        try:
            student = api.students.create(**student_data)
            student = Student(student)
            print(student)
        except Exception as e:
            if 'github_username' in e.error:
                messages = e.error['github_username']
                print(colored('\n'.join(messages), 'red'))
            else:
                print(colored('An unknown error occurred.', 'red'))
