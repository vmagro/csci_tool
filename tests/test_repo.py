import git

from csci_tool.config import Config
from csci_tool.student import Student
from csci_tool.repo import Repo


def test_clone_student_repo(mocker):
    """clone_student_repo creates tempdir and calls GitPython"""
    mocker.patch('git.Repo.clone_from')
    mocker.patch('csci_tool.config.Config.load_config')
    mock_config = mocker.MagicMock()
    Config.load_config.return_value = mock_config
    mock_config.github_org = 'test_org'
    s = Student(email='smagro@usc.edu', github='vmagro')
    tempdir = Repo.clone_student_repo(s)
    git.Repo.clone_from.assert_called_once_with(
        'git@github.com:test_org/hw_vmagro.git',
        tempdir)
