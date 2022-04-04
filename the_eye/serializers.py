from django.core.validators import MaxValueValidator
from django.utils import timezone
from rest_framework import serializers
from the_eye.models import Event


class EventSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(validators=[
        MaxValueValidator(
            limit_value=timezone.now,
            message='timestamp must be in the past')
    ])

    class Meta:
        model = Event
        fields = ['session_id', 'category', 'name', 'data', 'timestamp']
