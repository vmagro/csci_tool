import builtins
from mock import MagicMock
from pytest import fixture

from csci_tool.commands.base import BaseCommand


@fixture
def base_cmd():
    return BaseCommand()


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


def test_prompt_input_help(base_cmd, mocker):
    """help is printed when using input()"""
    base_cmd.OPTIONS = [
        ('e', '--example', 'example argument')
    ]

    mocker.patch('builtins.input')
    mock_args = MagicMock()
    builtins.input.return_value = 'from user input'
    del mock_args.example
    assert base_cmd.prompt(mock_args, 'example') == 'from user input'
    builtins.input.assert_called_once_with('example argument: ')


def test_populate_parser(base_cmd):
    """Populates subparser correctly"""
    base_cmd.NAME = 'base_test'
    base_cmd.HELP = 'base test help'
    base_cmd.OPTIONS = [
        ('e', '--example', 'example argument')
    ]
    subparsers = MagicMock()
    parser = MagicMock()
    subparsers.add_parser.return_value = parser

    base_cmd.populate_parser(subparsers)

    subparsers.add_parser.assert_called_once_with(
        'base_test', help='base test help'
    )
    parser.add_argument.assert_called_once_with(
        'e', '--example', help='example argument'
    )
