"""Code that supports creating a new course and GitHub stuff."""

import logging

from rest_framework.response import Response

from github import Github, GithubException

from .models import Course, CourseSetting


logger = logging.getLogger(__name__)


def setup_course(request):
    """Create a new course on the server.

    This includes making sure the appropriate GitHub teams exist, that push hooks are set up and
    that the bot account has a usable SSH key.
    """
    # first we need to add a new Course model to the db
    course = Course(name=request.data['name'])
    course.save()

    # now create any settings that we might have
    # some settings have sensible defaults, others do not
    settings = [('github_org', None), ('assignments_repo', 'assignments'), ('bot_email', None),
                ('bot_token', None), ('bot_username', None), ('bot_private_key', None),
                ('grader_team', 'graders'), ('student_repo_format', 'hw_{unix_name}'),
                ('student_description', 'Homework for {preferred_name} {last_name} <{usc_email}>'),
                ('comment_on_collect', True), ('private_repos', True)
                ]
    for key, default in settings:
        # use the value provided in the request or use the default here
        cs = CourseSetting(course=course, key=key, value=request.data.get(key, default))
        cs.save()

    settings = course.settings()
    github = Github(settings.bot_token)
    org = github.get_organization(settings.github_org)

    # Make a new SSH key for the bot and add it to GitHub

    # Check if the assignments repo exists and if not create it
    try:
        org.get_repo(settings.assignments_repo)
    except GithubException:
        private = settings.private_repos == 'True'
        org.create_repo(settings.assignments_repo, auto_init=True, private=private)
        pass

    # Check if the graders team exists and if not create it
    def ensure_grader_team():
        teams = org.get_teams()
        for team in teams:
            if team.name == settings.grader_team:
                logger.debug('Found grader team')
                return
        logger.warning('Grader team "%s" doesn\'t exist, making it now', settings.grader_team)
        org.create_team(settings.grader_team, permission='admin')
        logger.info('Created team "%s"', settings.grader_team)
    ensure_grader_team()

    # Check if the push hook exists and if not create it
    def ensure_hook():
        host = request.META['HTTP_HOST']
        hook_url = 'https://{}/gitbot/hook/push'.format(host)
        hooks = org.get_hooks()
        for hook in hooks:
            if hook.url == hook_url:
                logger.debug('Found existing hook')
                return
        logger.warning('Hook "%s" not found, making it now', hook_url)
        org.create_hook(name='web', config={
            'url': hook_url,
            'content_type': 'json',
        })
        logger.info('Created hook "%s"', hook_url)
    ensure_hook()

    return Response('OK')
