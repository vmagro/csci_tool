from .init import InitCommand
from .mutate import MutateCommand

subcommands = [
    InitCommand(),
    MutateCommand(),
]
