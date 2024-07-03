"""
Events application model tests
"""

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Event
from datetime import datetime
from datetime import timedelta
from django.utils import timezone

class TestEventModel(TestCase):

    def setUp(self):
        self.event_datetime = timezone.now() + timedelta(days=5)
        self.event = Event.objects.create(
            name='Base Event',
            friendly_name='Friendly Base Event',
            price=29.99,
            event_datetime=self.event_datetime,
            description='Description for Base Event',
            capacity=100,
            tickets_sold=50,
            image=None,
            alt_text='Alt text for Base Event',
            is_active=True
        )
    # Test event creation 
    def test_event_creation(self):
        self.assertIsInstance(self.event, Event)
        self.assertEqual(str(self.event), 'Base Event')
        self.assertEqual(self.event.friendly_name, 'Friendly Base Event')
        self.assertEqual(self.event.price, 29.99)      
        self.assertEqual(self.event.description, 'Description for Base Event')
        self.assertEqual(self.event.capacity, 100)
        self.assertEqual(self.event.tickets_sold, 50)
        self.assertEqual(self.event.event_datetime, self.event_datetime)     
   
    # Testing Event Order
    def test_event_ordering(self):
        self.event1 = Event.objects.create(
            name='Event 1',
            price=29.99,
            capacity=100,
            tickets_sold=50,
            event_datetime=timezone.now() - timedelta(days=1)
        )
        self.event2 = Event.objects.create(
            name='Event 2',
            price=29.99,
            capacity=100,
            tickets_sold=50,
            event_datetime=timezone.now()
        )
        self.event3 = Event.objects.create(
            name='Event 3',
            price=29.99,
            capacity=100,
            tickets_sold=50,
            event_datetime=timezone.now() + timedelta(days=1)
        )
        ordered_events = Event.objects.order_by('event_datetime')
        self.assertEqual(list(ordered_events), [self.event1, self.event2, self.event3, self.event])

    # Testing image upload works.
    def test_image_field(self):
        image_path = 'media/full-logo.png'
        with open(image_path, 'rb') as img:
            image_data = img.read()

        event_with_image = Event.objects.create(
            name='Event 1',
            friendly_name='Friendly Event 1',
            price=29.99,
            event_datetime=self.event_datetime,
            description='Description for Event 1',
            capacity=100,
            tickets_sold=50,
            image=SimpleUploadedFile('test_image.jpg', image_data, content_type='image/jpeg'),
            alt_text='Alt text for Event 1',
            is_active=True
        )

        saved_event = Event.objects.get(id=event_with_image.id)
        self.assertIsNotNone(saved_event.image)

    



