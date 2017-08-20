from io import StringIO
from mock import MagicMock

from csci_tool.commands.mutate import MutateCommand
from csci_tool.mutator import Mutator
from csci_tool.repo import Repo


def test_clone(mocker):
    """Clones student repos fresh from GitHub"""
    mocker.patch('csci_tool.repo.Repo.clone_student_repo')
    buf = StringIO('smagro@usc.edu vmagro\nsporkert@usc.edu esporkert')
    args = MagicMock()
    args.students = buf
    args.mutation = 'test_mutation'

    cmd = MutateCommand()
    cmd.run(args)

    Repo.clone_student_repo.assert_called_once_with('ssh://git@github.com:usc_csci356_fall17/hw_smagro.git')


def test_load_mutation(mocker):
    """Loads mutation from Mutator"""
    mocker.patch('csci_tool.mutator.Mutator.get_mutator')

    args = MagicMock()
    args.mutation = 'test_mutation'

    cmd = MutateCommand()
    cmd.run(args)

    Mutator.get_mutator.assert_called_once_with('test_mutation')


def test_mutation_no_func(mocker, capfd):
    """Logs error when no mutate function found"""
    mocker.patch('csci_tool.mutator.Mutator.get_mutator')
    Mutator.get_mutator.side_effect = AttributeError()

    args = MagicMock()
    args.mutation = 'test_mutation'

    cmd = MutateCommand()
    cmd.run(args)

    out, err = capfd.readouterr()
    assert err == 'mutate.py doesn\'t seem to have a mutate function\n'


def test_mutate_no_module(mocker, capfd):
    """Logs error when mutate.py not found"""
    mocker.patch('csci_tool.mutator.Mutator.get_mutator')
    Mutator.get_mutator.side_effect = OSError()

    args = MagicMock()
    args.mutation = 'test_mutation'

    cmd = MutateCommand()
    cmd.run(args)

    out, err = capfd.readouterr()
    assert err == 'Failed to import mutator "test_mutation", are you sure it exists?\n'  # noqa
