"""DRF Serializers for gitbot api."""

from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from rest_framework.serializers import ValidationError

from .models import Course, Student, Assignment
from . import github


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    """Seralizer class for the Course model."""
    class Meta:
        model = Course
        fields = ('name',)


class StudentSerializer(serializers.ModelSerializer):
    """Serializer class for Student model."""

    class Meta:
        model = Student
        fields = '__all__'

    def validate_github_username(self, username):
        """Check if the GitHub account actually exists."""
        exists = github.user_exists(username)
        if not exists:
            raise ValidationError('Github account "{}" doesn\'t exist'.format(username))
        return username


class AssignmentSerializer(NestedHyperlinkedModelSerializer):
    """Serializer class for Assignment model."""

    class Meta:
        model = Assignment
        fields = ('url', 'path', 'due_date', 'status')
