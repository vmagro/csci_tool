"""DRF Serializers for gitbot api."""

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from .models import Student
from . import github


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer class for Student model."""

    class Meta:
        model = Student
        fields = '__all__'

    def validate_github_username(self, username):
        """Check if the GitHub account actually exists."""
        exists = github.user_exists(username)
        if not exists:
            raise ValidationError(f'Github account "{username}" doesn\'t exist')
        return username
