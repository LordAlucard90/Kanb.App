from django.db import models
from django.utils import timezone


class Task(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=200, default='')
    created = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default='BACKLOG')

