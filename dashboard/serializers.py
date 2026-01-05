from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'status', 'created_at', 'scheduled_time', 'user']
        read_only_fields = ['user', 'created_at']
