from .collect import CollectCommand
from .create_repos import CreateReposCommand
from .login import LoginCommand
from .mutate import MutateCommand

subcommands = [
    CollectCommand(),
    CreateReposCommand(),
    LoginCommand(),
    MutateCommand(),
]
