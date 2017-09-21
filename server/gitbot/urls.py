"""URLs specific to gitbot."""
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views
from . import hooks

router = DefaultRouter(trailing_slash=False)
router.register(r'students', views.StudentViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^hook/push$', hooks.push_hook)
]
