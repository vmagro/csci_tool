"""API views for gitbot."""
from rest_framework import viewsets

from .models import Student
from .serializers import StudentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    """StudentViewSet, supports bulk upload of Student objects."""

    queryset = Student.objects.all()
    serializer_class = StudentSerializer
