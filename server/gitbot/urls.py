from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    url(r'^students$', views.StudentList.as_view()),
]
