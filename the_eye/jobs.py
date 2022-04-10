import json
import logging
from django_rq import job
from rest_framework import serializers

from the_eye.serializers import EventSerializer

logger = logging.getLogger(__name__)


@job
def save_event(data):
    """
    Save an event to the database or raise a ValidationError if data is invalid.
    """
    serializer = EventSerializer(data=data)
    if not serializer.is_valid():
        logger.error(json.dumps(data, indent=4, default=str))
        raise serializers.ValidationError(serializer.errors)
    serializer.save()
