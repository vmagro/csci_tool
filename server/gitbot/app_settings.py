"""A list of all the settings that can be customized for the gitbot app."""

from django.conf import settings

GITHUB_ORG = getattr(settings, 'GITBOT_GITHUB_ORG', 'usc-csci356-fall2017')
BOT_USERNAME = getattr(settings, 'GITBOT_BOT_USERNAME', 'vmagrobot')
BOT_ACCESSTOKEN = getattr(settings, 'GITBOT_BOT_ACCESS_TOKEN', None)

META_REPO_NAME = getattr(settings, 'GITBOT_META_REPO', 'meta')
GRADERS_TEAM = getattr(settings, 'GITBOT_GRADERS_TEAM', 'graders')
