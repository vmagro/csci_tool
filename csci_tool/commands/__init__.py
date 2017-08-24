from .collect import CollectCommand
from .create_repos import CreateReposCommand
from .login import LoginCommand
from .mutate import MutateCommand
from .grade import GradeCommand

subcommands = [
    CollectCommand(),
    CreateReposCommand(),
    LoginCommand(),
    MutateCommand(),
    GradeCommand(),
]
