#!/usr/bin/env python3

import argparse
import logging

from .api import Api
from .commands import subcommands

parser = argparse.ArgumentParser(
    description='Tool for managing USC CSCI course(s) GitHub repos'
)

parser.add_argument('--verbose', '-v', action='count', default=0)


def main():
    subparsers = parser.add_subparsers(dest='main_cmd', help='subcommand to run')
    subparsers.required = True
    for cmd in subcommands:
        cmd.populate_parser(subparsers)

    args = parser.parse_args()

    # warn is 30, should default to 30 when verbose=0
    # each level below warning is 10 less than the previous
    log_level = args.verbose*(-10) + 20
    logging.basicConfig(format='%(levelname)s:%(name)s: %(message)s',
                        level=log_level)

    logger = logging.getLogger(__name__)
    logger.info('Instantiating api client')
    api = Api(url='http://localhost:8080/gitbot/schema')

    args.main_cmd.run(api, args)


if __name__ == '__main__':
    main()
