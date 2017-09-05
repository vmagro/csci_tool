import git

from csci_tool.student import Student
from csci_tool.repo import Repo

from tests.mock_config import config
assert config is not None  # trick the linter that this is used


def test_clone_student_repo(mocker, config):
    """clone_student_repo creates tempdir and calls GitPython"""
    mocker.patch('git.Repo.clone_from')
    config.github_org = 'test_org'
    s = Student(email='smagro@usc.edu', github='vmagro')
    tempdir = Repo.clone_student_repo(s)
    git.Repo.clone_from.assert_called_once_with(
        'git@github.com:test_org/hw_smagro.git',
        tempdir)
