from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from .automation import run_email_task  # Example

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def run(self, request, pk=None):
        task = self.get_object()
        # In a real app, this would be offloaded to a queue (e.g., Celery)
        # Here we just run it synchronously for demonstration
        if "email" in task.name.lower():
             success = run_email_task(task.id)
        else:
             # Default mock run
             success = True
             task.status = 'completed'
             task.save()

        if success:
            return Response({'status': 'task execution started/completed'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'task failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
