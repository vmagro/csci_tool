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

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# we need to override some database settings since we use sqlite in development

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': 'localhost',
        'PORT': '',
    }
}
