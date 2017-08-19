class BaseCommand(object):
    """Superclass for all subcommands in csci_tool
    Provides some conveniences to read arguments from the user interactively or
    from the command line.
    """

    @staticmethod
    def unpack_option(opt):
        """Unpacks an option for argparse, with an optional kwargs"""
        # make it optional to have kwargs in case the help is not needed
        if len(opt) > 1:
            print(opt)
            args, kwargs = opt
        else:
            args = opt
            kwargs = {}
        return args, kwargs

    def populate_parser(self, subparsers):
        """Populate an subparser with the options for this subcommand"""
        parser = subparsers.add_parser(self.NAME, help=self.HELP)
        parser.set_defaults(command=self)
        options = getattr(self, 'OPTIONS', [])
        for opt in options:
            args, kwargs = self.unpack_option(opt)
            print(args, kwargs)
            parser.add_argument(*args, **kwargs)

    def run(self, args):
        """Run with the args from the subparser"""
        raise NotImplementedError('Subcommands must implement run()')

    def prompt(self, args, key):
        """Intelligently prompt the user for some data, first checking if it's
        already present in the arguments.
        """
        # find the help for the given argument, default to just the name
        help = key
        options = getattr(self, 'OPTIONS', [])
        for opt in options:
            args, kwargs = self.unpack_option(opt)
            short, long = args
            if 'help' in kwargs:
                cur_help = kwargs['help']
            else:
                cur_help = key
            if long == '--' + key:
                help = cur_help

        if hasattr(args, key) and getattr(args, key) is not None:
            return getattr(args, key)
        else:
            return input('{}: '.format(help))
