"""GitHub utils."""

from github import Github, GithubException

from .app_settings import BOT_ACCESSTOKEN

g = Github(BOT_ACCESSTOKEN)


def user_exists(username: str) -> bool:
    """Check if a user exists or not."""
    try:
        g.get_user(username)
        return True
    except GithubException:
        return False
    except:
        raise
