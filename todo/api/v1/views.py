from .serializers import TaskSerializer
from rest_framework import viewsets
from ...models import Task
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .paginations import DefaultPagination


class TaskModelViewSet(viewsets.ModelViewSet):
    """
    this is a view for showing list of task and create task
    and a view for showing task's detail and update it
    """

    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["is_complete"]
    search_fields = ["title"]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user.profile)
