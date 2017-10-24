import dateutil.parser


class Assignment(object):

    def __init__(self, d: dict):
        self.path = d['path']
        self.due_date = d['due_date']
        self.status = d['status']

    def __str__(self):
        date = dateutil.parser.parse(self.due_date)
        date = date.strftime('%a %b %y at %I:%M:%S %p')
        return f'{self.path} due at {date}: "{self.status}"'


class Submission(object):
    pass


class Mutation(object):
    pass


class Repo(object):
    pass


class Course(object):
    pass
