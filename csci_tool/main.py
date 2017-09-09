#!/usr/bin/env python3

import argparse
import logging
import os

# setup custom git ssh key if necessary
# this must happen before importing any commands that use GitPython
from .config import Config  # noqa
try:
    config = Config.load_config()
    if config.ssh_key is not None:
        os.environ['GIT_SSH_COMMAND'] = 'ssh -i ' + config.ssh_key

    from .repo import Repo  # noqa
    # before doing anything, check if we can update the meta repo
    meta_repo = Repo.meta_repo()
    meta_repo.remote().pull()
except:
    # fail silently
    pass

from .commands import subcommands  # noqa

parser = argparse.ArgumentParser(
    description='Tool for managing USC CSCI course(s) GitHub repos'
)

parser.add_argument('--verbose', '-v', action='count', default=0)


def main():
    subparsers = parser.add_subparsers(dest='command', help='subcommand to run')
    subparsers.required = True
    for cmd in subcommands:
        cmd.populate_parser(subparsers)

    args = parser.parse_args()

    # warn is 30, should default to 30 when verbose=0
    # each level below warning is 10 less than the previous
    log_level = args.verbose*(-10) + 20
    logging.basicConfig(format='%(levelname)s:%(name)s: %(message)s',
                        level=log_level)

    args.command.run(args)


if __name__ == '__main__':
    main()
