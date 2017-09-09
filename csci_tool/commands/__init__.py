from .collect import CollectCommand
from .collect_late import CollectLateCommand
from .create_repos import CreateReposCommand
from .login import LoginCommand
from .mutate import MutateCommand
from .grade import GradeCommand

subcommands = [
    CollectCommand(),
    CollectLateCommand(),
    CreateReposCommand(),
    LoginCommand(),
    MutateCommand(),
    GradeCommand(),
]
