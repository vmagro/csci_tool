"""
Local "production" settings for server app.

Based on the development settings, local mode is designed to require the least amount of setup
possible. We set celery to always be eager and we just use sqlite for the databajse
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# import all the options in settings and just override the ones we want
from .settings import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        # each request has a transaction, if the view raises and exception, it is rolled back
        'ATOMIC_REQUESTS': True,
    }
}

# this causes tasks to run in process
CELERY_TASK_ALWAYS_EAGER = True
