"""GitHub utils."""

import logging
from github import Github, GithubException

from .app_settings import BOT_ACCESSTOKEN, GITHUB_ORG, GRADERS_TEAM, HOOK_URL

logger = logging.getLogger(__name__)


g = Github(BOT_ACCESSTOKEN)

org = g.get_organization(GITHUB_ORG)


def user_exists(username: str) -> bool:
    """Check if a user exists or not."""
    try:
        g.get_user(username)
        return True
    except GithubException:
        return False
    except:
        raise


def ensure_grader_team():
    """Check if the graders team exists and if not create it."""
    teams = org.get_teams()
    for team in teams:
        if team.name == GRADERS_TEAM:
            logger.debug('Found grader team')
            return
    logger.warning('Grader team "%s" doesn\'t exist, making it now', GRADERS_TEAM)
    org.create_team(GRADERS_TEAM, permission='admin')
    logger.info('Created team "%s"', GRADERS_TEAM)


def ensure_hook():
    """Check if the push hook exists and if not create it."""
    hooks = org.get_hooks()
    for hook in hooks:
        if hook.url == HOOK_URL:
            logger.debug('Found existing hook')
            return
    logger.warning('Hook "%s" not found, making it now', HOOK_URL)
    org.create_hook(name='web', config={
        'url': HOOK_URL,
        'content_type': 'json',
    })
    logger.info('Created hook "%s"', HOOK_URL)
