"""API views for gitbot."""
from rest_framework import viewsets
from django.http import StreamingHttpResponse
from rest_framework.decorators import detail_route

from .models import Course, Student, Assignment
from .serializers import CourseSerializer, StudentSerializer, AssignmentSerializer
from .setup_course import setup_course
from . import tasks


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def create(self, request):
        """Proxy create to the setup_course function which will interact with GitHub."""
        return setup_course(request)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class AssignmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Assignment.objects.all().order_by('-due_date')
    serializer_class = AssignmentSerializer

    @detail_route(methods=['POST'])
    def deploy(self, request, pk=None):
        """Deploy assignment to student repos."""
        assignment = self.get_object()

        if request.data.get('canary', False):
            students = Student.objects.filter(canary=True)
        else:
            students = Student.objects.all()

        task_group = tasks.give_assignment_to_all(students, assignment)

        def stream_generator():
            def cb(task_id, value):
                print('Got task result')
                yield '{}\n'.format(task_id)
            print('joining')
            yield task_group.get(callback=cb)
            print('joined')

        content = stream_generator()
        return StreamingHttpResponse(streaming_content=content)

    @detail_route(methods=['POST'])
    def collect(self, request, pk=None):
        """Collect assignment from student repos."""
        assignment = self.get_object()

        if request.data.get('canary', False):
            students = Student.objects.filter(canary=True)
        else:
            students = Student.objects.all()

        task_group = tasks.collect_assignment_from_all(students, assignment)

        def stream_generator():
            def cb(task_id, value):
                print('Got task result')
                yield '{}\n'.format(task_id)
            print('joining')
            yield task_group.get(callback=cb)
            print('joined')

        content = stream_generator()
        return StreamingHttpResponse(streaming_content=content)
