from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal
from products.models import Product, Event, ProductVariant


class TestBagView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.product = Product.objects.create(friendly_name='Test Product')
        self.variant = ProductVariant.objects.create(product=self.product, size='M', price=Decimal('5.00'))
        
    # render the correct template
    def test_view_bag(self):
        response = self.client.get(reverse('view_bag'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bag/bag.html')

    # Add product to bag
    def test_add_product_to_bag(self):
        response = self.client.post(reverse('add_product_to_bag', args=[self.product.id]), {
            'quantity': 1,
            'redirect_url': reverse('view_bag'),
            'product_type': 'product',
            'variant_id': self.variant.id,
            'card_message': 'Happy Birthday',
            'note_to_seller': 'No green'
        })
        self.assertRedirects(response, reverse('view_bag'))
        bag = self.client.session['bag']
        unique_key = f"{self.product.id}_{self.variant.id}_Happy Birthday_No green"
        self.assertIn(unique_key, bag)
        self.assertEqual(bag[unique_key]['quantity'], 1)


    
    def test_update_card_message(self):
        # add a product to the bag
        self.client.post(reverse('add_product_to_bag', args=[self.product.id]), {
            'quantity': 1,
            'redirect_url': reverse('view_bag'),
            'product_type': 'product',
            'variant_id': self.variant.id,
            'card_message': 'Happy Birthday',
            'note_to_seller': 'No green'
        })
        unique_key = f"{self.product.id}_{self.variant.id}_Happy Birthday_No green"
        # Update the card message
        response = self.client.post(reverse('update_card_message', args=[self.product.id]), {
            'new_card_message': 'I Love You!',
            'unique_key': unique_key,
            'variant_id': self.variant.id,
            'note_to_seller': 'No green'
        })
        self.assertRedirects(response, reverse('view_bag'))
        bag = self.client.session['bag']
        new_unique_key = f"{self.product.id}_{self.variant.id}_I Love You!_No green"
        self.assertIn(new_unique_key, bag)
        self.assertEqual(bag[new_unique_key]['card_message'], 'I Love You!')