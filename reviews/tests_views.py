from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from checkout.models import Order
from profiles.models import UserProfile
from .models import Review
from django.test import Client


class TestReviewViews(TestCase):
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

        # Create an Order instance
        self.order = Order.objects.create(
            user_profile=self.user_profile,
            email='test@example.com',
            full_name='Test User',
            phone_number='1234567890',
            postcode='12345',
            town_or_city='Test Town',
            street_address1='123 Test Street',
            street_address2='Bristol',
            county='Test County',
            stripe_pid='test_pid',
            original_bag='{}'
        )

        # Initialize the client and login the user
        self.client = Client()
        self.client.login(username='testuser9', password='password9')

    def test_review_order_view(self):
        """
        Test that the review order page can be accessed and reviewed correctly.
        """
        response = self.client.get(reverse('review_order', args=[self.order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/review_order.html')
        self.assertContains(response, self.user_profile.user.username)

    def test_successful_review_submission(self):
        """
        Test that a review can be successfully submitted.
        """
        response = self.client.post(reverse('review_order', args=[self.order.id]), {
            'review_text': 'This is a valid review text.'
        })
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after successful submission
        self.assertTrue(Review.objects.filter(user=self.user, order=self.order).exists())
        
