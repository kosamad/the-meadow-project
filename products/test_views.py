from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Product, Event, ProductVariant, Category
from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
import uuid


"""
Products tests
"""
class TestProductViews(TestCase):

    def setUp(self):
        # Set up a category for the product
        self.category = Category.objects.create(
            name='Test Category',
            friendly_name='Test Category'
        )

        # Set up an image 
        image_path = 'media/full-logo.png'
        with open(image_path, 'rb') as img:
            image_data = img.read()

        # Create a product instance
        self.product = Product.objects.create(
            id=uuid.uuid4(),
            category=self.category,
            name='Test Product',
            friendly_name='Test Product',
            price=19.99,
            description='This is a test product description.',
            image=SimpleUploadedFile('test_image.jpg', image_data, content_type='image/jpeg'),
            alt_text='Test Product Image',
            is_gift_card=False,
            is_active=True,
            is_infinite_stock=False
        )

        # Create a product variant
        self.variant = ProductVariant.objects.create(
            product=self.product,
            size='M',
            stock=10,
            is_infinite_stock=False,
            price=19.99,
            is_active=True
        )

    def test_get_product_detail_page(self):
        url = reverse('product_detail', args=[self.product.id])
        response = self.client.get(url)
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')
        
        # Check that the product details are correct in the response
        self.assertContains(response, self.product.name)
        self.assertContains(response, self.product.description)
        self.assertContains(response, self.product.price)
        self.assertContains(response, self.variant.get_size_display())
        self.assertContains(response, self.variant.price)
        self.assertContains(response, self.product.alt_text)

"""
Events tests
"""


class TestEventViews(TestCase):

    def setUp(self):     

        # Set up category "event"
        self.category = Category.objects.create(
            name='Event',
            friendly_name='Event'
        )

        # Set up an image
        image_path = 'media/full-logo.png'
        with open(image_path, 'rb') as img:
            image_data = img.read()

        # Set up date/time
        self.event_datetime = timezone.now() + timedelta(days=5)

        # Create an event instance
        self.event = Event.objects.create(
            id=uuid.uuid4(),
            category=self.category,
            name='Test Event',
            friendly_name='Test Event',
            price=29.99,
            event_datetime=self.event_datetime,
            duration_hours=2,
            description='This is a test event description.',
            image=SimpleUploadedFile('test_image.jpg', image_data, content_type='image/jpeg'),
            alt_text='Test Event Image',
            is_active=True
        )

    def test_get_event_detail_page(self):
        url = reverse('event_detail', args=[self.event.id])
        response = self.client.get(url)
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/event_detail.html')
        
        # Check that the event details are correct in the response 
        self.assertContains(response, self.event.name)
        self.assertContains(response, self.event.description)
        self.assertContains(response, self.event.price)
        self.assertContains(response, self.event.alt_text)       