import json

from django.test import TestCase

from the_eye.models import Event
from the_eye.serializers import EventSerializer


class EventListTests(TestCase):
    def test_create_event(self):
        response = self.client.post(
            '/events/', 
            {
                'session_id': '123',
                'category': 'test',
                'name': 'test',
                'data': json.dumps({'test': 'test'}),
                'timestamp': '2022-01-01 00:00:00.000000'
            }
        )
        self.assertEqual(response.status_code, 201)

    def test_list_events(self):
        Event.objects.bulk_create(
            [
                Event(session_id='123', category='test', name='test', data=json.dumps({'test': f'test{i}'}))
                for i in range(10)
            ]
        )
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [EventSerializer(event).data for event in Event.objects.all().iterator()])
