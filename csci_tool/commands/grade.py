import argparse
import logging
from os import path

from .base import BaseCommand
from ..config import Config
from ..grader import Grader
from ..repo import Repo


logger = logging.getLogger(__name__)


class GradeCommand(BaseCommand):
    NAME = 'grade'
    HELP = 'run auto grading scripts or run convenience grading scripts for \
human grading'

    def populate_args(self):
        self.add_argument('auto', help='run auto grading scripts',
                          action='store_true')
        self.add_argument('assignment', help='assignment name')
        self.add_argument('students', help='students file', nargs='?',
                          type=argparse.FileType('r'),
                          default=None)

    def run(self, args):
        assignment = args.assignment

        meta_repo = Repo.meta_rep()
        meta_dir = meta_repo.working_tree_dir
        if args.students is None and not args.auto:
            # if we're running in human grader mode and didn't get a
            # students.txt then use the students.txt generated for the current
            # grader by their USC unix name
            my_name = Config.load_config().unix_name
            default = path.join(meta_dir, 'submissions', 'assingment',
                                'grade_' + my_name + '.txt')
            print('Loading students to grade for ' + my_name)
            with open(default, 'r') as students_file:
                students = self.load_students(students_file)
        else:
            students = self.load_students(args)

        logger.info('Collecting from %d students', len(students))

        logger.info('Updating meta repo')
        meta_repo.remote().pull()
        # TODO(vmagro) does this also pull down submodules?

        # run auto grader or human grading script and write to grades.csv
        for student in students:
            grader = Grader.get_grader(assignment)
            if args.auto:
                logger.info('Auto-grading %s', student.unix_name)
                # run auto grader script and write out a line of CSV
                score, max_score = grader.auto_grade
                print(score, max_score)
            else:
                # show the relevant files to a human
                # wait for them to give a score, then write out a line of CSV
                max_score = 10
                score = input('score out of {}: '.format(max_score))
                return (score, max_score)

        # done grading, commit our changes
        meta_repo.index.add([path.join('submissions', assignment, 'grades.csv')])
        meta_repo.index.commit('Graded {} for {} students'
                               .format(assignment, len(students)))
        logger.info('Pushing changes to meta repo')
        meta_repo.remote().push()
