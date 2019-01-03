from django.db.models.signals import post_save
from django.dispatch import receiver
from . import models, serializers


@receiver(post_save, sender=models.Task)
def log_task_change(sender, instance, created, **kwargs):
    x = models.Event()
    t = serializers.TaskSerializer(instance=instance)

    if created:
        x.name = "CREATED"
    else:
        x.name = "UPDATED"
    x.save()
