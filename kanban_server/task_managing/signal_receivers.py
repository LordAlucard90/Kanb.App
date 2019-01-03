import json
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.forms import model_to_dict

from . import models, serializers


@receiver(post_save, sender=models.Task)
def log_task_change(sender, instance: models.Task, created, **kwargs):
    x = models.Event()
    # t = serializers.TaskSerializer(instance=instance)

    if created:
        x.name = "CREATED"
    else:
        x.name = "UPDATED"

    x.object_id = instance.id
    # x.JSON = serializers.TaskSerializer(instance=instance)
    d = model_to_dict(instance)
    d['created'] = str(instance.created.isoformat())
    d['due_date'] = str(instance.created.isoformat())
    d['status'] = ('BACKLOG', 'TODO')
    x.JSON = json.dumps(d)
    x.save()
