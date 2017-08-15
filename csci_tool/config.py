"""
Configuration loader
Loads an INI config file (.cscirc) to determine application settings, starting
by looking in the current directory, then up a level recursively until found or
reaches '/', then looks in the user's homedir
"""

from configparser import ConfigParser
import errno
import logging
import os
from os import path


logger = logging.getLogger(__name__)


def find_config(d):
    """Find the .cscirc config file relevant to this project
    This recurses up to parent directories until reaching /, returning the first
    .cscirc found, or ~/.cscirc

    Args:
        d (str): directory to start searching (usually cwd)
    Returns:
        PathLike path to config file to use
    """
    logger.debug('Checking for %s/.cscirc', d)
    if path.isfile(path.join(d, '.cscirc')):
        logger.debug('Found .cscirc in %s', d)
        return path.join(d, '.cscirc')
    elif path.dirname(d) == d:
        # don't go up past /
        # default to ~/.cscirc
        return path.join(path.expanduser('~'), '.cscirc')
    else:
        parent = path.dirname(d)
        logger.debug('Didn\'t find .cscirc in %s, checking %s', d, parent)
        return find_config(parent)


def load_config():
    f = find_config(os.getcwd())
    if f is None:
        raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), '.cscirc')
    config = ConfigParser()
    config.read(f)
    return config


def update_config(config):
    config.write(path)
