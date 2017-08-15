import os

from csci_tool.config import find_config, load_config

# make the linter happy
FileNotFoundError = OSError


def test_not_found(fs):
    """find_config defaults to ~/.cscirc"""
    fs.MakeDirectories('/test/config/project/subdir')
    os.chdir('/test/config/project/subdir')
    d = os.getcwd()
    assert find_config(d) == os.path.join(os.path.expanduser('~'), '.cscirc')


def test_cwd(fs):
    """finds config file in current directory"""
    fs.MakeDirectories('/test/config/project/subdir')
    os.chdir('/test/config/project/subdir')
    fs.CreateFile('/test/config/project/subdir/.cscirc')
    assert load_config() is not None, 'should have loaded config'


def test_grandparent(fs):
    """finds config file in grandparent directory"""
    fs.MakeDirectories('/test/config/project/subdir')
    os.chdir('/test/config/project/subdir')
    fs.CreateFile('/test/config/.cscirc')
    # make sure we're really getting the grandparent cscirc
    assert not fs.Exists('/test/config/project/subdir/.cscirc')
    assert load_config() is not None, 'should have loaded config'
