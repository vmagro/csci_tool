#!/usr/bin/env python3

import argparse
from .commands import subcommands

parser = argparse.ArgumentParser(
    description='Tool for managing USC CSCI course(s) GitHub repos'
)


def main():
    subparsers = parser.add_subparsers(dest='command', help='subcommand to run')
    subparsers.required = True
    for cmd in subcommands:
        cmd.populate_parser(subparsers)

    args = parser.parse_args()

    args.command.run(args)


if __name__ == '__main__':
    main()
