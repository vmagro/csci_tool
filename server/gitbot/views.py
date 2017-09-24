"""API views for gitbot."""
from rest_framework import viewsets

from .models import Student, Assignment
from .serializers import StudentSerializer, AssignmentSerializer

import time
from rest_framework.decorators import api_view
from django.http import StreamingHttpResponse


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class AssignmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer


@api_view(['GET', 'POST'])
def stream_test(request):
    def gen():
        i = 0
        while True:
            print(i)
            time.sleep(0.5)
            i += 1
            yield '{}\r\n\r'.format(i)
    print('calling gen')
    content = gen()
    print('got generator')
    return StreamingHttpResponse(streaming_content=content)
