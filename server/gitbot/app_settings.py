"""A list of all the settings that can be customized for the gitbot app."""

from django.conf import settings

CLASS_NAME = getattr(settings, 'GITBOT_CLASS_NAME', 'CS356')
GITHUB_ORG = getattr(settings, 'GITBOT_GITHUB_ORG', 'usc-csci356-fall2017')
BOT_EMAIL = getattr(settings, 'GITBOT_BOT_EMAIL', 'v+gitbot@vinnie.io')
BOT_USERNAME = getattr(settings, 'GITBOT_BOT_USERNAME', 'vmagrobot')
BOT_ACCESSTOKEN = getattr(settings, 'GITBOT_BOT_ACCESS_TOKEN', None)
BOT_PRIVATE_KEY_PATH = getattr(settings, 'GITBOT_BOT_PRIVATE_KEY_PATH', None)

ASSIGNMENTS_REPO_NAME = getattr(settings, 'GITBOT_ASSIGNMENTS_REPO', 'assignments')
ASSIGNMENTS_REPO_URL = 'git@github.com/{}:{}.git'.format(GITHUB_ORG, ASSIGNMENTS_REPO_NAME)
ASSIGNMENTS_REPO_PATH = getattr(settings, 'GITBOT_ASSIGNMENTS_REPO_PATH', '/tmp/assignments_repo')
GRADERS_TEAM = getattr(settings, 'GITBOT_GRADERS_TEAM', 'graders')


STUDENT_REPO_NAME_FORMAT = getattr(settings, 'GITBOT_STUDENT_REPO_NAME', 'hw_{unix_name}')
STUDENT_DESCRIPTION_FORMAT = getattr(settings, 'GITBOT_STUDENT_DESCRIPTION',
                                     'Homework for {preferred_name} {last_name} <{usc_email}>')
