"""HTML/API views for gitbot."""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from .models import Student


class StudentList(APIView):
    """A view that returns a templated HTML representation of a given Student."""

    queryset = Student.objects.all()
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request):
        """Return HTML for all students."""
        return Response({'students': self.queryset.all()}, template_name='students/list.html')
