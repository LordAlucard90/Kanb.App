from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        read_only_fields = ('created',)
        fields = (
            'title', 'description', 'status', 'owner', 'created',
            'due_date', 'work_points', 'category'
        )
