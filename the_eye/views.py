from rest_framework import generics

from the_eye.serializers import EventSerializer
from the_eye.models import Event


class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
