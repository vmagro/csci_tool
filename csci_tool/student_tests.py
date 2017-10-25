from .student import Student

from pytest import fixture
from . import course_settings


@fixture
def student():
    return Student(
        usc_email='smagro@usc.edu',
        usc_id=1234,
        first_name='Stephen',
        last_name='Magro',
        preferred_name='Vinnie',
        github_username='vmagro',
    )


def test_repo_name(mocker, student):
    """Repo name uses course settings."""
    mocker.patch('csci_tool.course_settings.CourseSettings.get_settings')
    mock_settings = mocker.MagicMock()
    course_settings.CourseSettings.get_settings.return_value = mock_settings
    mock_settings.student_repo_format = 'repo_{preferred_name}_{last_name}'
    assert student.repo_name == 'repo_vinnie_magro'


def test_repo_url(mocker, student):
    """Repo URL uses course settings."""
    mocker.patch('csci_tool.course_settings.CourseSettings.get_settings')
    mock_settings = mocker.MagicMock()
    course_settings.CourseSettings.get_settings.return_value = mock_settings
    mock_settings.bot_username = 'user'
    mock_settings.bot_token = 'token'
    mock_settings.github_org = 'org'
    mock_settings.student_repo_format = 'repo_{preferred_name}_{last_name}'
    assert student.repo_url == 'https://user:token@github.com/org/repo_vinnie_magro.git'
