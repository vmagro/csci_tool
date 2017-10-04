"""URLs specific to gitbot."""
from django.conf.urls import url, include
from rest_framework_nested.routers import SimpleRouter, NestedSimpleRouter

from rest_framework.schemas import get_schema_view

from . import views
from . import hooks

router = SimpleRouter(trailing_slash=False)
router.register(r'courses', views.CourseViewSet)
course_router = NestedSimpleRouter(router, r'courses', lookup='course')
course_router.register(r'students', views.StudentViewSet, base_name='course-students')
course_router.register(r'assignments', views.AssignmentViewSet, base_name='course-assignments')

schema_view = get_schema_view(title='Gitbot API')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(course_router.urls)),
    url(r'^hook/push$', hooks.push_hook),
    url(r'^schema/$', schema_view),
]
