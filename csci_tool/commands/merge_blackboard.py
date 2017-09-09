import argparse
import logging
import csv

from .base import BaseCommand


logger = logging.getLogger(__name__)


class MergeBlackboardCommand(BaseCommand):
    NAME = 'merge-blackboard'
    HELP = 'merge grades.csv with blackboard csv'

    def populate_args(self):
        self.add_argument('blackboard', help='blackboard csv',
                          type=argparse.FileType('r'))
        self.add_argument('csci', help='csci generated grades',
                          type=argparse.FileType('r'))
        self.add_argument('output', help='output file',
                          type=argparse.FileType('w'))
        self.add_argument('columns', nargs='+',
                          help='column names mapped from grades.csv')

    def run(self, args):
        student_grades = {}
        csci = csv.DictReader(args.csci, fieldnames=['unixname'] + args.columns)
        for line in csci:
            student = line['unixname']
            del line['unixname']
            student_grades[student] = line

        blackboard = csv.DictReader(args.blackboard)
        fields = blackboard.fieldnames
        # there's some weird unicode bs in the first column of a blackboard file
        # this grabs just the actual column
        fields[0] = fields[0][2:-1]
        output = csv.DictWriter(args.output, fieldnames=blackboard.fieldnames)
        output.writeheader()
        for row in blackboard:
            unix_name = row['Username']
            new_row = row
            new_row.update(student_grades[unix_name])
            output.writerow(new_row)
