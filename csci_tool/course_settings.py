class CourseSettings(object):

    __slots__ = ('course', 'settings')

    def __init__(self, course):
        """Load settings from a Course model."""
        self.course = course
        # get all the settings at initialization time
        self.settings = {}
        for s in course.coursesetting_set.all():
            self.settings[s.key] = s.value

    def __getitem__(self, key):
        """Allow subscript notation to access settings."""
        return self.get(key)

    # this allows us to do something like settings.github_org to get the github_org setting
    def __getattr__(self, key):
        """Allow dot notation to access settings."""
        return self.get(key)

    def get(self, key, default=None):
        """Allow dict-style .get to access settings."""
        val = self.settings.get(key, default)
        if val == 'True':
            return True
        elif val == 'False':
            return False
        return val
