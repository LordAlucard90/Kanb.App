from django.db import models
from django.utils import timezone


class Task(models.Model):
    STATUS_LIST = ('BACKLOG', 'TODO', 'WORKING', 'VERIFY', 'COMPLETED', 'WAIT')
    STATUS_CHOICES = ((x, x,) for x in STATUS_LIST)

    title = models.CharField(max_length=20)
    description = models.CharField(max_length=200, default='')
    created = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(default=None, null=True, blank=True)
    status = models.CharField(max_length=20, default=STATUS_LIST[0], choices=STATUS_CHOICES)
    owner = models.CharField(max_length=50, default='')
    work_points = models.PositiveSmallIntegerField(default=0)
    category = models.CharField(max_length=40, default='UNCATEGORIZED')
