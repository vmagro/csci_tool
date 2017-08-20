from csci_tool.mutator import Mutator


def test_load(fs):
    """Loads mutator from subdirectory"""
    fs.CreateFile('/Users/vmagro/tmp/csci_356_meta/test/mutate.py',
                  contents='''
def mutate(student):
    pass
''')
    assert Mutator.get_mutator('test') is not None


def test_load_not_found(fs):
    """Raises an error when mutate.py not found"""
    pass


def test_load_not_subclass(fs):
    """Raises an error when mutate.py doesn't export a subclass of Mutator"""
    pass
