"""Tests for repo functionality."""
from gitbot.repo import LocalRepo

import os
import tempfile
import shlex
import subprocess


def run_shell(cmd, cwd=None):
    """Run cmd as a string and return stdout."""
    if cwd is None:
        cwd = os.getcwd()
    output = subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE, cwd=cwd).stdout
    output = output.decode('utf-8').strip()
    return output


def test_run(mocker):
    """Make sure that the process is run in the repo dir and pipes stdout/err."""
    mocker.patch('subprocess.run')
    repo = LocalRepo('/tmp')

    repo.run(['echo', 'true'])

    subprocess.run.assert_called_once_with(['echo', 'true'], check=True, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, cwd='/tmp')


def test_commit(mocker):
    """Test that a commit is made and has the correct author and commmit information."""
    with tempfile.TemporaryDirectory() as dirname:
        # make a repo dir and 'git init' it
        subprocess.run(['git', 'init'], cwd=dirname)
        # instantiate the LocalRepo
        repo = LocalRepo(dirname)
        # make a commit
        repo.commit('vmagrobot', 'v+gitbot@vinnie.io', 'test_commit commit message')

        # verify the commit information by shelling out to git
        commit_message = run_shell('git show --format="%s" -s HEAD', cwd=dirname)
        assert commit_message == 'test_commit commit message', 'Commit message incorrect'
        author_email = run_shell('git show --format="%ae" -s HEAD', cwd=dirname)
        assert author_email == 'v+gitbot@vinnie.io', 'Author email incorrect'
        author_name = run_shell('git show --format="%an" -s HEAD', cwd=dirname)
        assert author_name == 'vmagrobot', 'Author name incorrect'
