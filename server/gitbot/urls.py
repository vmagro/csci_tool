"""URLs specific to gitbot."""
from django.conf.urls import url

from . import views
from . import hooks

urlpatterns = [
    url(r'^students$', views.StudentList.as_view()),
    url(r'^hook/push$', hooks.push_hook)
]
