from mock import MagicMock

from csci_tool.repo import Repo
from csci_tool.commands.create_repos import CreateReposCommand

from tests.mock_config import config
assert config is not None  # trick the linter that this is used


def test_write_students_initial(mocker, fs, config):
    """Students list is created when it doesn't exist"""
    # setup the mocked repo
    fs.MakeDirectories('/test/meta')
    mocker.patch('csci_tool.repo.Repo.meta_repo')
    config.meta_path = '/test/meta/'
    mock_repo = MagicMock()
    Repo.meta_repo.return_value = mock_repo
    mock_repo.working_tree_dir = '/test/meta/'

    # setup a fake file with student info
    args = MagicMock()
    test_contents = '''smagro@usc.edu vmagro
sporkert@usc.edu esporkert
'''
    fs.CreateFile('students_input.txt', contents=test_contents)
    # argparse automatically opens the file
    args.students = open('students_input.txt', 'r')

    cmd = CreateReposCommand()
    cmd.run(args)

    # make sure that the file exists
    assert fs.Exists('/test/meta/students.txt')
    # make sure the contents are what we expected
    contents = open('/test/meta/students.txt').read()
    assert contents == test_contents


def test_write_students_append(mocker, fs, config):
    """Students list is appended to if it already exists"""
    # setup the mocked repo
    fs.MakeDirectories('/test/meta')
    mocker.patch('csci_tool.repo.Repo.meta_repo')
    config.meta_path = '/test/meta/'
    mock_repo = MagicMock()
    Repo.meta_repo.return_value = mock_repo
    mock_repo.working_tree_dir = '/test/meta/'

    # setup a fake file with student info
    args = MagicMock()
    test_contents = '''picus@usc.edu spicus'''
    fs.CreateFile('students_input.txt', contents=test_contents)
    # argparse automatically opens the file
    args.students = open('students_input.txt', 'r')

    # fake the meta repo students.txt with initial data
    fs.CreateFile('/test/meta/students.txt',
                  contents='''smagro@usc.edu vmagro
sporkert@usc.edu esporkert
''')

    cmd = CreateReposCommand()
    cmd.run(args)

    # make sure that the file exists
    assert fs.Exists('/test/meta/students.txt')
    # make sure the contents are what we expected
    contents = open('/test/meta/students.txt').read()
    assert contents == '''smagro@usc.edu vmagro
sporkert@usc.edu esporkert
picus@usc.edu spicus
'''

def test_commit(mocker):
    # TODO(vmagro) test that a commit with the changes was made
    pass
