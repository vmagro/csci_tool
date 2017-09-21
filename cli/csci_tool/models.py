class Student(object):

    def __init__(self, d: dict):
        self.usc_email = d['usc_email']
        self.usc_id = d['usc_id']
        self.preferred_name = d['preferred_name']
        self.first_name = d['first_name']
        self.last_name = d['last_name']
        self.github_username = d['github_username']


    def __str__(self):
        return f'{self.preferred_name} {self.last_name} <{self.usc_email}>'
