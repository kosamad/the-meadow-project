"""
 Shop application view tests
"""

from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
import uuid
from datetime import timedelta
from django.utils import timezone
from products.models import Category, Product, Event, ProductVariant


class TestShopViews(TestCase):

    def setUp(self):
        # Define image data (empty content for the sake of the test)
        self.image_data = b''
        self.category = Category.objects.create(name='Test Category')
        # Create a product instance
        self.product = Product.objects.create(
            id=uuid.uuid4(),
            category=self.category,
            name='Test Product',
            friendly_name='Test Product',
            price=19.99,
            description='This is a test product description.',
            image=SimpleUploadedFile(
                'test_image.jpg',
                self.image_data,
                content_type='image/jpeg'
                ),
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

        # Create a inactive product instance
        self.inactive_product = Product.objects.create(
            id=uuid.uuid4(),
            category=self.category,
            name='Inactive Product',
            friendly_name='Inactive Product',
            price=19.99,
            description='This is a Inactive Product description.',
            image=SimpleUploadedFile(
                'test_image.jpg',
                self.image_data,
                content_type='image/jpeg'
                ),
            alt_text='Inactive Product Image',
            is_gift_card=False,
            is_active=False,
            is_infinite_stock=False
        )

        # Define a datetime for the event
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
            image=SimpleUploadedFile(
                'test_image.jpg',
                self.image_data,
                content_type='image/jpeg'
                ),
            alt_text='Test Event Image',
            is_active=True
        )

    # Check basic shop view
    def test_shop_view_no_filters(self):
        url = reverse('shop')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/shop.html')

        # checking data rendered to the template (Context)
        self.assertIn('combined_list', response.context)

        # check all products/events are on the page (should be 2)
        combined_list = response.context['combined_list']
        self.assertEqual(len(combined_list), 2)

    # Check shop view with a search
    def test_shop_view_with_search_query(self):
        url = reverse('shop') + '?q=Test'
        response = self.client.get(url)
        combined_list = response.context['combined_list']
        for item in combined_list:
            if item['item_type'] == 'Product':
                self.assertIn('test', item['item'].name.lower())
            elif item['item_type'] == 'Event':
                self.assertIn('test', item['item'].name.lower())

    # Check shop view with a category filter selected

    def test_shop_view_with_category_filter(self):
        url = reverse('shop') + '?category=Test Category'
        response = self.client.get(url)
        combined_list = response.context['combined_list']
        for item in combined_list:
            if item['item_type'] == 'Product':
                self.assertEqual(item['item'].category.name, 'Test Category')
