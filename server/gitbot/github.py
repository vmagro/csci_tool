"""GitHub utils."""

import logging
from github import Github, GithubException

logger = logging.getLogger(__name__)


def user_exists(username: str) -> bool:
    """Check if a user exists or not."""
    try:
        logger.debug('Checking if GitHub account %s exists', username)
        # we don't need a logged-in user for this - do anonymously to keep things simple
        Github().get_user(username)
        return True
    except GithubException:
        logger.debug('It didn\'t :(', username)
        return False
    except:
        raise
