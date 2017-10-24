#!/usr/bin/env python3

import logging
import click
import os

from .commands import subcommands


@click.group()
@click.option('-v', '--verbose', count=True)
@click.option('--config', default=os.path.expanduser('~/.cscirc'))
@click.pass_context
def cli(ctx, verbose, config):
    """Set up course and logging level."""
    # warn is 30, should default to 30 when verbose=0
    # each level below warning is 10 less than the previous
    log_level = verbose*(-10) + 20
    logging.basicConfig(format='%(levelname)s:%(name)s: %(message)s',
                        level=log_level)


for sub in subcommands:
    cli.add_command(sub)
