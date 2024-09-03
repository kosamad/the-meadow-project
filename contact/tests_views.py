from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from django.contrib.auth.models import User
from profiles.models import UserProfile
from checkout.models import Order


class ContactViewTests(TestCase):

    def setUp(self):
        # Create or retrieve a User instance
        self.user, created = User.objects.get_or_create(username="testuser9")
        if created:
            self.user.set_password("password9")
            self.user.save()

        # Create or retrieve a UserProfile instance associated with the User
        self.user_profile, _ = UserProfile.objects.get_or_create(
            user=self.user,
            defaults={
                'default_phone_number': '1234567890',
                'default_postcode': '12345',
                'default_town_or_city': 'Test Town',
                'default_street_address1': '123 Test Street',
                'default_street_address2': 'Bristol',
                'default_county': 'Test County',
            }
        )

        # Initialize the client and login the user
        self.client = Client()
        self.client.login(username='testuser9', password='password9')

    def test_contact_get_authenticated(self):
        """Test contact page GET request when user is authenticated"""
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')
        self.assertIn('orders', response.context)
        # Check if user has orders
        self.assertEqual(len(response.context['orders']), 0)  # No orders created in this test

    def test_contact_get_unauthenticated(self):
        """Test contact page GET request when user is not authenticated"""
        self.client.logout()  # Ensure user is not logged in
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')
        self.assertIn('orders', response.context)
        self.assertEqual(response.context['orders'], [])
