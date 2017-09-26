"""
Production settings for server app.

Based on the normal settings, we just override the options we want to change in prod.
"""

import os

# import all the options in settings and just override the ones we want
from .settings import *  # noqa

# DEBUG in prod is very bad
DEBUG = False

# makes cookies harder to sniff
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# we don't use iframes so just deny all requests
X_FRAME_OPTIONS = 'DENY'
# enable xss protection
SECURE_BROWSER_XSS_FILTER = True

# force SSL - in practice nginx will do this but this makes security warnings go away
SECURE_SSL_REDIRECT = True

# this keeps browsers from guessing the content type if the header isn't set
SECURE_CONTENT_TYPE_NOSNIFF = True

# we're using docker secrets which will store the content in files under /run/secrets
SECRET_KEY = os.environ['DJANGO_SECRET']


# we need to override some database settings since we use sqlite in development

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'csci_tool',
        'USER': 'csci_tool',
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': 'db',
        'PORT': '',
    }

}

# we also need to override some celery options since redis is in a separate containers
CELERY_BROKER_URL = 'redis://redis'

# we want to be able to collect static files so that nginx knows what to do with them
STATIC_ROOT = 'static'
