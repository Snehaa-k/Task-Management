from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'assigned_to', 'due_date', 'status', 'completion_report', 'worked_hours', 'created_at', 'updated_at']
        read_only_fields = ('created_at', 'updated_at')

class TaskCompletionSerializer(serializers.ModelSerializer):
    completion_report = serializers.CharField(required=True)
    worked_hours = serializers.DecimalField(max_digits=5, decimal_places=2, required=True)
    
    class Meta:
        model = Task
        fields = ['status', 'completion_report', 'worked_hours']
        
    def validate_status(self, value):
        if value != 'completed':
            raise serializers.ValidationError("Status must be 'completed'")
        return value

class TaskReportSerializer(serializers.ModelSerializer):
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'assigned_to_username', 'completion_report', 'worked_hours', 'updated_at']
