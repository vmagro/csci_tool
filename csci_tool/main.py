#!/usr/bin/env python3

import logging
import click

from .api import Api
from .commands import subcommands


@click.group()
@click.option('-v', '--verbose', count=True)
@click.option('--api', default='http://localhost:8001/gitbot/schema')
@click.pass_context
def cli(ctx, verbose, api):
    """Set up api client and logging level."""
    # warn is 30, should default to 30 when verbose=0
    # each level below warning is 10 less than the previous
    log_level = verbose*(-10) + 20
    logging.basicConfig(format='%(levelname)s:%(name)s: %(message)s',
                        level=log_level)

    logger = logging.getLogger(__name__)

    logger.debug('Instantiating api client')
    ctx.obj = Api(url=api)


for sub in subcommands:
    cli.add_command(sub)
