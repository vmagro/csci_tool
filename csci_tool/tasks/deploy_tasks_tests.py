"""Tests for assignment deploy tasks."""

from pytest import fixture
import tempfile
import subprocess
import os

from .deploy_tasks import clone_repo, mutate_repo
from ..repo import LocalRepo


@fixture
def student(mocker):
    """Create a mock student with enough data for all the deploy tasks."""
    s = mocker.Mock(spec=['repo', 'unix_name'])
    s.unix_name = 'unix'
    s.repo = mocker.Mock(spec=['student', 'repo_url'])
    s.repo.student = s
    s.repo.repo_url = 'someurl'
    return s


@fixture
def course(mocker):
    """Create a mock Course."""
    c = mocker.Mock(spec=['settings'])
    mock_settings = mocker.Mock(spec=['assignments_repo_path'])
    mock_settings.assignments_repo_path = '/tmp'
    c.settings.return_value = mock_settings
    return c


@fixture
def assignment(mocker, course):
    """Create a mock assignment that has enough data for the tasks under test."""
    a = mocker.Mock(spec=['name', 'path', 'course'])
    a.path = 'test-assignment'
    a.name = 'test-assignment'
    a.course = course
    return a


def test_clone_repo(mocker, student):
    """clone_repo clones a student repo in a temp dir."""
    mocker.patch('gitbot.repo.LocalRepo.clone_repo')
    clone_repo(student)
    assert gitbot.repo.LocalRepo.clone_repo.called_once_with(student.repo)


def test_mutate_repo(mocker, assignment, student):
    """mutate_repo runs the mutate function and makes a new commit."""
    mock_import_mutate = mocker.patch('gitbot.assignment_utils.import_mutate')

    ran_in = None

    def side_effect(*args):
        nonlocal ran_in
        ran_in = os.getcwd()
        # on mac, cwd will have /private in front but otherwise the path is the same
        if ran_in.startswith('/private'):
            ran_in = ran_in[len('/private'):]
        return 'test commit message'

    mock_mutate = mocker.MagicMock(side_effect=side_effect)
    mock_import_mutate.return_value = mock_mutate

    # create a fake LocalRepo
    with tempfile.TemporaryDirectory() as dirname:
        # make a repo dir and 'git init' it
        subprocess.run(['git', 'init'], cwd=dirname)
        # instantiate the LocalRepo
        repo = LocalRepo(dirname)

        ret_repo, commit_message = mutate_repo(repo, assignment, student)

        mock_mutate.assert_called_once_with(student, os.path.join(dirname, '/tmp/test-assignment'))
        assert ran_in == os.path.join(dirname, 'test-assignment')

        assert commit_message == 'test commit message'
        assert ret_repo == repo
