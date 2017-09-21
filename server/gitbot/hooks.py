"""GitHub web hooks."""

from datetime import datetime
import logging

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Repo, Commit

logger = logging.getLogger(__name__)


@api_view(['POST'])
def push_hook(request):
    """Handle a push hook for a repo in our organization."""
    # only do anything if this is a change to the master branch
    if request.data['ref'] != 'refs/heads/master':
        logger.warning('Not a commit on the master branch, just ignore it')
        return Response('OK')

    # get the repo that this hook was for
    repo_name = request.data['repository']['name']
    try:
        repo = Repo.objects.get(pk=repo_name)
    except:
        logger.warning('Failed to find repo "%s", ignoring this hook', repo_name)
        return Response('OK')

    # create new commits in the database based on what was pushed
    # we might lose a few commits since the webhook includes a maximum of 20 but that's ok
    if 'commits' in request.data:
        for d in request.data['commits']:
            logger.debug('Saving commit: %s', d)
            commit = Commit(repo=repo, sha=d['id'], author=d['author']['username'],
                            commit_date=d['timestamp'], push_date=datetime.now(),
                            message=d['message'])
            commit.save()

    return Response('OK')
