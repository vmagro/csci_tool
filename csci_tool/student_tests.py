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
        github_userame='vmagro',
    )


def test_repo_name(mocker, student):
    """Repo URL uses course settings."""
    mocker.mock('course_settings.get_settings')
    mock_settings = mocker.MagicMock()
    course_settings.get_settings.return_value = mock_settings
    mock_settings.bot_username = 'user'
    mock_settings.bot_token = 'token'
    mock_settings.github_org = 'org'
    mock_settings.student_repo_format = 'repo_{preferred_name}_{last_name}'
    assert student.github_repo_url == 'asdf'
