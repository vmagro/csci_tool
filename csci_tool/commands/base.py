class BaseCommand(object):
    """Superclass for all subcommands in csci_tool
    Provides some conveniences to read arguments from the user interactively or
    from the command line.
    """

    def populate_parser(self, subparsers):
        """Populate an subparser with the options for this subcommand"""
        parser = subparsers.add_parser(self.NAME, help=self.HELP)
        parser.set_defaults(command=self)
        options = getattr(self, 'OPTIONS', [])
        for opt in options:
            short, long, help = opt
            parser.add_argument(short, long, help=help)

    def run(self, args):
        """Run with the args from the subparser"""
        raise NotImplemented('Subcommands must implement run()')

    def prompt(self, args, key):
        """Intelligently prompt the user for some data, first checking if it's
        already present in the arguments.
        """
        # find the help for the given argument, default to just the name
        help = key
        options = getattr(self, 'OPTIONS', [])
        for opt in options:
            short, long, cur_help = opt
            if long == '--' + key:
                help = cur_help

        if hasattr(args, key) and getattr(args, key) is not None:
            return getattr(args, key)
        else:
            return input('{}: '.format(help))
