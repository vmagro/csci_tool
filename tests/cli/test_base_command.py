import builtins
from mock import MagicMock
from pytest import fixture

from csci_tool.commands.base import BaseCommand


@fixture
def base_cmd():
    return BaseCommand()

@fixture
def subparsers():
    subparsers = MagicMock()
    parser = MagicMock()
    subparsers.add_parser.return_value = parser
    return subparsers, parser


def test_prompt_cmd(base_cmd):
    """Picks variables out of command line args"""
    mock_args = MagicMock()
    mock_args.provided_on_cmd = 'cmd'
    assert base_cmd.prompt(mock_args, 'provided_on_cmd') == 'cmd'


def test_prompt_input(base_cmd, mocker):
    """Picks variables from input() if not in command line"""
    mocker.patch('builtins.input')
    mock_args = MagicMock()
    builtins.input.return_value = 'from user input'
    del mock_args.interactively
    assert base_cmd.prompt(mock_args, 'interactively') == 'from user input'
    builtins.input.assert_called_once_with('interactively: ')


def test_prompt_input_help(subparsers, mocker):
    """help is printed when using input()"""
    subparsers, parser = subparsers
    class Sub(BaseCommand):
        NAME = 'base_test'
        HELP = 'base test help'

        def populate_args(self):
            self.add_argument('-e', '--example', help='example argument')

    cmd = Sub()
    cmd.populate_parser(subparsers)

    mocker.patch('builtins.input')
    mock_args = MagicMock()
    builtins.input.return_value = 'from user input'
    del mock_args.example
    assert cmd.prompt(mock_args, 'example') == 'from user input'
    builtins.input.assert_called_once_with('example argument: ')


def test_populate_parser(subparsers):
    """Populates subparser correctly"""
    subparsers, parser = subparsers
    class Sub(BaseCommand):
        NAME = 'base_test'
        HELP = 'base test help'

        def populate_args(self):
            self.add_argument('-e', '--example', help='example argument')

    cmd = Sub()
    cmd.populate_parser(subparsers)

    subparsers.add_parser.assert_called_once_with(
        'base_test', help='base test help'
    )
    parser.add_argument.assert_called_once_with(
        '-e', '--example', help='example argument'
    )
