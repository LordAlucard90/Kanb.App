from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import viewsets

from .serializers import TaskSerializer
from .models import Task


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class BoardView(TemplateView):
    template_name = 'board.html'
    extra_context = {'title': 'Main board'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()
        context['columns'] = Task.STATUS_LIST
        return context
