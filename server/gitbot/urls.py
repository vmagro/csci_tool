"""URLs specific to gitbot."""
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from rest_framework.schemas import get_schema_view

from . import views
from . import hooks

router = DefaultRouter(trailing_slash=False)
router.register(r'students', views.StudentViewSet)
router.register(r'assignments', views.AssignmentViewSet)

schema_view = get_schema_view(title='Gitbot API')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^hook/push$', hooks.push_hook),
    url(r'^schema/$', schema_view),
]
