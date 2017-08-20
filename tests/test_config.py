import os

from csci_tool.config import Config

# make the linter happy
FileNotFoundError = OSError


def test_not_found(fs):
    """find_config defaults to ~/.csci/cscirc"""
    fs.MakeDirectories('/test/config/project/subdir')
    os.chdir('/test/config/project/subdir')
    d = os.getcwd()
    c = Config.find_config(d)
    assert c == os.path.join(os.path.expanduser('~'), '.csci', 'cscirc')


def test_cwd(fs):
    """finds config file in current directory"""
    fs.MakeDirectories('/test/config/project/subdir')
    os.chdir('/test/config/project/subdir')
    fs.CreateFile('/test/config/project/subdir/.cscirc')
    assert Config.load_config() is not None, 'should have loaded config'


def test_grandparent(fs):
    """finds config file in grandparent directory"""
    fs.MakeDirectories('/test/config/project/subdir')
    os.chdir('/test/config/project/subdir')
    fs.CreateFile('/test/config/.cscirc')
    # make sure we're really getting the grandparent cscirc
    assert not fs.Exists('/test/config/project/subdir/.cscirc')
    assert Config.load_config() is not None, 'should have loaded config'
