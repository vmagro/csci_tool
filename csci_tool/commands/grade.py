import argparse
import logging
import csv
import subprocess
import os
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
        self.add_argument('--auto', help='run auto grading scripts',
                          action='store_true')
        self.add_argument('assignment', help='assignment name')
        self.add_argument('students', help='students file', nargs='?',
                          type=argparse.FileType('r'),
                          default=None)

    def run(self, args):
        assignment = args.assignment

        meta_repo = Repo.meta_repo()
        meta_dir = meta_repo.working_tree_dir
        if args.students is None and not args.auto:
            # if we're running in human grader mode and didn't get a
            # students.txt then use the students.txt generated for the current
            # grader by their USC unix name
            my_name = Config.load_config().unix_name
            default = path.join(meta_dir, 'submissions', assignment,
                                'grade_' + my_name + '.txt')
            print('Loading students to grade for ' + my_name)
            with open(default, 'r') as students_file:
                students = self.load_students(students_file)
        else:
            students = self.load_students(args.students)

        logger.info('Grading for %d students', len(students))

        # TODO(vmagro) make sure that all submodules of meta repo are downloaded

        # run auto grader or human grading script and write to grades.csv
        try:
            grader = Grader.get_grader(assignment)
        except:
            logger.error('Failed to import grader "%s", are you sure it exists?',
                         assignment)
            return
        # source_dir is where the grader files exist in the meta repo
        source_dir = path.join(meta_dir, assignment)

        # set up grades.csv if it is not set up
        os.chdir(source_dir)
        if args.auto:
            f = open('grades.csv', 'a', newline='')
        else:
            f = open('grades_human.csv', 'a', newline='')
        writer = csv.writer(f)
        # run the grader
        for student in students:
            student_submission = path.join(meta_dir, 'submissions', assignment,
                                           student.unix_name, assignment)
            if args.auto:
                logger.info('Auto-grading %s', student.unix_name)
                cwd = os.getcwd()
                os.chdir(student_submission)
                # run auto grader script and write out a line of CSV
                scores =  grader.auto_grade(student, source_dir)
                os.chdir(cwd)
                # write to grades.csv
                writer.writerow([student.unix_name] + scores)
            else:
                # show the relevant files to a human
                # wait for them to give a score, then write out a line of CSV
                cwd = os.getcwd()
                os.chdir(student_submission)
                list = grader.human_grade(student, source_dir)
                os.chdir(cwd)
                for i in list[1]:
                    shell_output = subprocess.Popen('subl ' + i, shell=True, stdout=subprocess.PIPE, cwd=student_submission)
                    output = shell_output.stdout.read()
                    output = output.decode("utf-8")
                    print (output)
                    score = input('score out of {}: '.format(list[0]))
                    writer.writerow([student.repo_name] + [score])

        # done grading, commit our changes
        f.close()
        if args.auto:
            meta_repo.index.add([path.join(meta_dir, 'submissions', assignment, 'grades.csv')])
            meta_repo.index.commit('Auto-Graded {} for {} students'
                                   .format(assignment, len(students)))
        else:
            meta_repo.index.add([path.join(meta_dir, 'submissions', assignment, 'grades_human.csv')])
            meta_repo.index.commit('Human-Graded {} for {} students'
                                   .format(assignment, len(students)))
        logger.info('Pushing changes to meta repo')
        meta_repo.remote().push()
