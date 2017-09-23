"""API views for gitbot."""
from rest_framework import viewsets

from .models import Student
from .serializers import StudentSerializer

import time
from rest_framework.decorators import api_view
from django.http import StreamingHttpResponse


class StudentViewSet(viewsets.ModelViewSet):
    """StudentViewSet, supports bulk upload of Student objects."""

    queryset = Student.objects.all()
    serializer_class = StudentSerializer


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
