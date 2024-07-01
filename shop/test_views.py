"""
 Shop application view tests
"""

from django.test import TestCase
from django.urls import reverse
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from products.models import Category, Product
from events.models import Event

class TestShopViews(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            friendly_name='Test Product',
            price=19.99,
            description='This is a test product description.',
            has_sizes=True,
            alt_text='Test Product Image',
            rating=4.5,
            is_gift_card=False,
            is_active=True,
            size='M',
            image=None
        )
        self.event_datetime = timezone.now() + timedelta(days=5)
        self.event = Event.objects.create(
            name='Test Event',
            friendly_name='Test Event',
            price=29.99,
            event_datetime=self.event_datetime,
            description='This is a test event description.',
            capacity=100,
            tickets_sold=50,
            alt_text='Test Event Image',
            is_active=True,
            image=None
        )

    # Check basic shop view
    def test_shop_view_no_filters(self):
        url = reverse('shop')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/shop.html')

        # checking data rendered to the template (Context)
        self.assertIn('categories', response.context)
        self.assertIn('combined_list', response.context)
        self.assertIn('search_term', response.context)
        self.assertIn('selected_category', response.context)

        # check all products/events are on the page (should be 2)
        combined_list = response.context['combined_list']
        self.assertEqual(len(combined_list), 2)

        # Check alphabetical sorting
        combined_list_sorted = sorted(combined_list, key=lambda x: x['item'].friendly_name.lower())
        self.assertEqual(combined_list_sorted[0]['item'].name, 'Test Event')
        self.assertEqual(combined_list_sorted[1]['item'].name, 'Test Product')


    # Check shop view with a search
    def test_shop_view_with_search_query(self):
        url = reverse('shop') + '?q=roses'  
        response = self.client.get(url)        
        combined_list = response.context['combined_list']
        for item in combined_list:
            if item['item_type'] == 'Product':
                self.assertIn('roses', item['item'].name.lower())
            elif item['item_type'] == 'Event':
                self.assertIn('roses', item['item'].name.lower())

    # Check shop view with a category filter selected
    def test_shop_view_with_category_filter(self):
        url = reverse('shop') + '?category=plants'
        response = self.client.get(url)       
        combined_list = response.context['combined_list']
        for item in combined_list:
            if item['item_type'] == 'Product':
                self.assertEqual(item['item'].category.name, 'plants')
    
    