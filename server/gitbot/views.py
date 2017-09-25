"""API views for gitbot."""
from rest_framework import viewsets
from django.http import StreamingHttpResponse
from rest_framework.decorators import detail_route

from .models import Student, Assignment
from .serializers import StudentSerializer, AssignmentSerializer
from . import tasks


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class AssignmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Assignment.objects.all().order_by('-due_date')
    serializer_class = AssignmentSerializer

    @detail_route(methods=['POST'])
    def deploy(self, request, pk=None):
        """Deploy assignment to all student repos."""
        assignment = self.get_object()

        # TODO: support canarying
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
