# tasks/views.py
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer, TaskCompletionSerializer, TaskReportSerializer
from .permissions import IsSuperAdminOrAdmin

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Task.objects.all()
        elif getattr(user, 'role', None) == 'admin':
            return Task.objects.filter(assigned_to__admin=user)
        else:
            return Task.objects.filter(assigned_to=user)

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsSuperAdminOrAdmin()]
        elif self.action in ['update', 'partial_update']:
            if self.request.data.get('status') == 'completed':
                return [IsAuthenticated()]  
            return [IsSuperAdminOrAdmin()]
        return [IsAuthenticated()]

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        if request.data.get('status') == 'completed':
            serializer = TaskCompletionSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['get'], url_path='report', permission_classes=[IsSuperAdminOrAdmin])
    def get_report(self, request, pk=None):
        task = self.get_object()
        if task.status != 'completed':
            return Response({'error': 'Task not completed'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = TaskReportSerializer(task)
        return Response(serializer.data)
