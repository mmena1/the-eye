from django.core.validators import MaxValueValidator, URLValidator
from django.utils import timezone
from rest_framework import serializers

from the_eye.models import Event


class OptionalSchemeURLValidator(URLValidator):
    """
    A URL validator that allows the scheme to be omitted.
    """
    def __call__(self, value):
        if '://' not in value:
            value = 'https://' + value
        super(OptionalSchemeURLValidator, self).__call__(value)


class PayloadSerializer(serializers.Serializer):
    """
    The parent serializer for an event's payload.
    """
    host = serializers.CharField(required=True, max_length=200, validators=[OptionalSchemeURLValidator()])
    path = serializers.CharField(required=True, max_length=200)


class PageInteractionPageViewSerializer(PayloadSerializer):
    """
    The serializer for a page interaction event with the name 'page_view'.
    """
    pass


class PageInteractionCtaClickSerializer(PayloadSerializer):
    """
    The serializer for a page interaction event with the name 'cta_click'.
    """
    element = serializers.CharField(max_length=100)


class FormInteractionSubmitSerializer(PayloadSerializer):
    """
    The serializer for a form interaction event with the name 'submit'.
    """
    form = serializers.JSONField()


PAYLOAD_SERIALIZERS = {
    ('page_interaction', 'page_view'): PageInteractionPageViewSerializer,
    ('page_interaction', 'cta_click'): PageInteractionCtaClickSerializer,
    ('form_interaction', 'submit'): FormInteractionSubmitSerializer
}


class EventSerializer(serializers.ModelSerializer):
    """
    The serializer for an event.
    """
    timestamp = serializers.DateTimeField(required=True, validators=[
        MaxValueValidator(
            limit_value=timezone.now,
            message='timestamp must be in the past')
    ])

    class Meta:
        model = Event
        exclude = ['id']
        extra_kwargs = {'category': {'required': True}}
        extra_kwargs = {'name': {'required': True}}
        extra_kwargs = {'data': {'required': True}}
        extra_kwargs = {'session_id': {'required': True}}

    def validate(self, attrs):
        """
        Validate the payload of the event.
        """
        category = attrs.get('category')
        name = attrs.get('name')
        try:
            data_serializer = PAYLOAD_SERIALIZERS[(category, name)]
        except KeyError:
            raise serializers.ValidationError(f'unknown event type: {category} - {name}')
        else:
            data = attrs.get('data')
            if data:
                serializer = data_serializer(data=data)
                serializer.is_valid(raise_exception=True)
            return attrs
