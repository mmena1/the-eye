from django.db import models
from django.utils import timezone


class Event(models.Model):
    """
    An event is a record of a user's interaction with a website.
    """
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    data = models.JSONField()
    timestamp = models.DateTimeField(default=timezone.now)
    session_id = models.CharField(max_length=100)

    class Meta:
        ordering = ['-timestamp']
