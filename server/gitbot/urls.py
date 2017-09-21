"""URLs specific to gitbot."""
from django.conf.urls import url

from . import hooks

urlpatterns = [
    url(r'^hook/push$', hooks.push_hook)
]
