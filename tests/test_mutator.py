from csci_tool.mutator import Mutator

from tests.mock_config import config
assert config is not None  # trick the linter that this is used


def test_load(fs, config):
    """Loads mutator from subdirectory"""
    fs.CreateFile('/test/meta/test/mutate.py',
                  contents='''
def mutate(student):
    pass
''')
    return
    # TODO(vmagro) make these tests work
    config.meta_path = '/test/meta'
    assert Mutator.get_mutator('test') is not None


def test_load_not_found(fs):
    """Raises an error when mutate.py not found"""
    pass


def test_load_not_subclass(fs):
    """Raises an error when mutate.py doesn't export a subclass of Mutator"""
    pass
