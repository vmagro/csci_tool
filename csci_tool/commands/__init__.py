from .collect import CollectCommand
from .collect_late import CollectLateCommand
from .create_repos import CreateReposCommand
from .login import LoginCommand
from .mutate import MutateCommand

subcommands = [
    CollectCommand(),
    CollectLateCommand(),
    CreateReposCommand(),
    LoginCommand(),
    MutateCommand(),
]
