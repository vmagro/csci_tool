"""Tests for repo functionality."""
from gitbot.repo import LocalRepo

import subprocess


def test_run(mocker):
    """Make sure that the process is run in the repo dir and pipes stdout/err."""
    mocker.patch('subprocess.run')
    repo = LocalRepo()
    repo.path = '/tmp'

    repo.run(['echo', 'true'])

    subprocess.run.assert_called_once_with(['echo', 'true'], check=True, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, cwd='/tmp', env={})
