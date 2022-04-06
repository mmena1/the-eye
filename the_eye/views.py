from rest_framework import generics

from the_eye.serializers import EventSerializer
from the_eye.models import Event


class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        session = self.request.query_params.get('session_id')
        category = self.request.query_params.get('category')
        start_time = self.request.query_params.get('start_time')
        end_time = self.request.query_params.get('end_time')
        queryset = Event.objects.all()
        if session:
            queryset = queryset.filter(session_id=session)
        if category:
            queryset = queryset.filter(category=category)
        if start_time and end_time:
            queryset = queryset.filter(timestamp__range=(start_time, end_time))
        return queryset
