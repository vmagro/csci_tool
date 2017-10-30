import argparse
import logging
from os import path

from .base import BaseCommand
from ..config import Config
from ..repo import Repo
from ..student import Student


logger = logging.getLogger(__name__)


class CollectLateCommand(BaseCommand):
    NAME = 'collect-late'
    HELP = 'collect student repos as submodules for an assignment, using specific SHAs'

    def populate_args(self):
        self.add_argument('assignment', help='assignment name')
        self.add_argument('submissions', help='submissions file', nargs='?',
                          type=argparse.FileType('r'),
                          default=None)

    def run(self, args):
        assignment = args.assignment
        logger.info('Collecting late submissions for %s', assignment)

        meta_repo = Repo.meta_repo()
        config = Config.load_config()
        github = config.github

        failures = []

        for line in args.submissions:
            email, late_days, sha = line.strip().split(',')
            logger.info('Collecting %s from %s for %s, %s late day(s)',
                        sha, email, assignment, late_days)
            # there will already be a submodule for them, so we need to update
            # it instead, and then leave a comment on their GitHub
            try:
                student = Student(email, None)

                sub_name = '{}_{}'.format(assignment, student.unix_name)

                try:
                    sub = meta_repo.submodule(sub_name)
                except:
                    # if the submodule couldn't be found, create it
                    dest_dir = path.join('submissions', assignment, student.unix_name)
                    sub = meta_repo.create_submodule(
                        name=sub_name,
                        path=dest_dir,
                        url=student.repo_url
                    )

                logger.debug('Updating submodule')
                sub.update(init=True, force=True)
                logger.debug('Switching submodule to %s', sha)
                sub.module().git.checkout(sha)
                logger.debug('Adding to index')
                # this magic incantation is required to get GitPython to commit
                sub.binsha = sub.module().head.commit.binsha
                meta_repo.index.add([sub])

                # comment on the commit that we collected
                repo_fqn = config.github_org + '/' + student.repo_name
                # must use fully qualified repo name with org
                repo = github.get_repo(repo_fqn)
                commit = repo.get_commits(sha=sha)[0]
                comment = 'This commit was collected as part of "{}". \n \
This was a late submission using {} late day(s). If you think this is \
incorrect, please post on Piazza.'.format(assignment, late_days)
                logger.debug('Commenting on GitHub')
                commit.create_comment(comment)
            except Exception as e:
                logger.error('Failed for %s, %s', email, e)
                failures.append((email, late_days, sha))

        if failures:
            logger.error('Failed on %d students, please try them again', len(failures))
            logger.error('Failures have been written out to ./failures.txt')
            with open('failures.txt', 'w') as f:
                for s in failures:
                    f.write('{},{},{}\n'.format(email, late_days, sha))

        # commit all the submissions at once

        logger.info('Committing/pushing to meta repo')
        meta_repo.index.commit('Collected late projects for {}'
                               .format(assignment))
        meta_repo.remote().push()
