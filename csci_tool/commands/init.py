from .base import BaseCommand


class InitCommand(BaseCommand):
    NAME = 'init'
    HELP = 'setup a new repository'
    OPTIONS = [
        ('-g', '--github', 'GitHub username'),
    ]

    def run(self, args):
        self.prompt(args, 'github', 'github username')
