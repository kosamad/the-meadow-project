from django.test import TestCase
from django.contrib.auth.models import User
from checkout.models import Order, ProductOrderLineItem, EventOrderLineItem
from .models import Review
from profiles.models import UserProfile


class ReviewModelTest(TestCase):

    def setUp(self):

        # Create or retrieve a User instance (prevent unique contraint errors)
        self.user, created = User.objects.get_or_create(username="testuser8")
        if created:
            self.user.set_password("password8")
            self.user.save()

        # Create or retrieve a UserProfile instance associated with the User
        self.user_profile, _ = UserProfile.objects.get_or_create(user=self.user)

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

        # Create a Review instance
        self.review = Review.objects.create(
            user=self.user,
            order=self.order,
            review_text='This is a test review.'
        )

    def test_review_creation(self):
        """
        Test that a Review instance is created correctly.
        """
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.order, self.order)
        self.assertEqual(self.review.review_text, 'This is a test review.')
