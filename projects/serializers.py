from rest_framework import serializers
from .models import Project, Task


# Сериализатор для модели Project
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_by', 'created_at']


# Сериализатор для модели Task
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'project',
            'is_completed',
            'assigned_to',
            'created_at',
        ]
