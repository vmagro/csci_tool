from .create_repos import CreateReposCommand
from .login import LoginCommand
from .mutate import MutateCommand

subcommands = [
    CreateReposCommand(),
    LoginCommand(),
    MutateCommand(),
]
