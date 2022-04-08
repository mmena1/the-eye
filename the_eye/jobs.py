from django_rq import job

from the_eye.serializers import EventSerializer


@job
def save_event(data):
    serializer = EventSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
