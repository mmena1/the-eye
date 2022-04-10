import json

from django.test import TestCase
from django.utils import timezone

from the_eye.models import Event
from the_eye.serializers import (
    EventSerializer,
    FormInteractionSubmitSerializer,
    PageInteractionCtaClickSerializer,
    PageInteractionPageViewSerializer,
    PayloadSerializer
)


class EventSerializerTestCase(TestCase):
    def setUp(self):
        self.timestamp = timezone.now()
        self.event = Event.objects.create(
            session_id='123',
            category='page_interaction',
            name='page_view',
            data={
                "host": "www.consumeraffairs.com",
                "path": "/",
            },
            timestamp=self.timestamp
        )

    def test_event_serializer_serialize(self):
        serializer = EventSerializer(self.event)
        self.assertEqual(serializer.data['session_id'], self.event.session_id)
        self.assertEqual(serializer.data['category'], self.event.category)
        self.assertEqual(serializer.data['name'], self.event.name)
        self.assertEqual(serializer.data['data'], self.event.data)
        self.assertEqual(serializer.data['timestamp'], str(self.event.timestamp))

    def test_event_serializer_deserialize(self):
        serializer = EventSerializer(
            data={
                'session_id': '123',
                'category': 'page_interaction',
                'name': 'page_view',
                'data': {
                    "host": "www.consumeraffairs.com",
                    "path": "/",
                },
                'timestamp': self.timestamp
            }
        )
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['session_id'], self.event.session_id)
        self.assertEqual(serializer.validated_data['category'], self.event.category)
        self.assertEqual(serializer.validated_data['name'], self.event.name)
        self.assertEqual(serializer.validated_data['data'], self.event.data)
        self.assertEqual(serializer.validated_data['timestamp'], self.event.timestamp)

    def test_event_serializer_validate_timestamp(self):
        serializer = EventSerializer(
            self.event,
            data={
                'session_id': '123',
                'category': 'test',
                'name': 'test',
                'data': json.dumps({'test': 'test'}),
                'timestamp': timezone.now() + timezone.timedelta(days=1)
            }
        )
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['timestamp'], ['timestamp must be in the past'])

    def test_event_serializer_validate_payload(self):
        serializer = EventSerializer(
            self.event,
            data={
                'session_id': '123',
                'category': 'test',
                'name': 'test',
                'data': json.dumps({'test': 'test'}),
                'timestamp': self.timestamp
            }
        )
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['non_field_errors'], ['unknown event type: test - test'])

    def test_event_serializer_validate_required_fields(self):
        serializer = EventSerializer(
            data={}
        )
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['category'], ['This field is required.'])
        self.assertEqual(serializer.errors['name'], ['This field is required.'])
        self.assertEqual(serializer.errors['data'], ['This field is required.'])
        self.assertEqual(serializer.errors['timestamp'], ['This field is required.'])
        self.assertEqual(serializer.errors['session_id'], ['This field is required.'])

    def test_payload_host_valid_without_url_scheme(self):
        serializer = PayloadSerializer(
            data={
                'host': 'www.url.com',
                'path': '/'
            }
        )
        self.assertTrue(serializer.is_valid())

    def test_payload_host_valid_with_url_scheme(self):
        serializer = PayloadSerializer(
            data={
                'host': 'http://www.url.com',
                'path': '/'
            }
        )
        self.assertTrue(serializer.is_valid())

    def test_page_interaction_page_view_serializer(self):
        serializer = PageInteractionPageViewSerializer(
            data={
                    'host': 'www.url.com',
                    'path': '/'
                }
        )
        self.assertTrue(serializer.is_valid())

    def test_page_interaction_cta_click_serializer(self):
        serializer = PageInteractionCtaClickSerializer(
            data={
                    'host': 'www.url.com',
                    'path': '/',
                    'element': 'button'
            }
        )
        self.assertTrue(serializer.is_valid())

    def test_form_interaction_submit_serializer(self):
        serializer = FormInteractionSubmitSerializer(
            data={
                    'host': 'www.url.com',
                    'path': '/',
                    'form': {
                        'name': 'Foo',
                        'lastname': 'Bar'
                    }
            }
        )
        self.assertTrue(serializer.is_valid())
