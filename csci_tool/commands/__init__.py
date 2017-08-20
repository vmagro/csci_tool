from .create_repos import CreateReposCommand
from .init import InitCommand
from .mutate import MutateCommand

subcommands = [
    CreateReposCommand(),
    InitCommand(),
    MutateCommand(),
]
