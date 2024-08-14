from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.messages import get_messages
from .models import UserProfile
from .forms import UserProfileForm
from checkout.models import Order

# Create your tests here.

"""
Profile tests
"""
class TestProfileView(TestCase):

    def setUp(self):
        # Create a user and profile (PLEASE CHANGE USERNAME AND PW TO GET TEST TO PASS)
        #otherwise this will fail the Unique contraint
        self.user = User.objects.create_user(username='newtest1', password='newtestpass1')        
        self.client = Client()
        self.client.login(username='newtest1', password='newtestpass1')

    # Profile loads with correct data
    def test_profile_page_loads(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.user.email)

    # Profile updates 
    def test_profile_update_success(self):
        form_data = {
            'default_phone_number': '1234',
            'default_town_or_city': 'Test town',
        }
        response = self.client.post(reverse('profile'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Profile updated successfully')

        updated_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(updated_profile.default_phone_number, '1234')
        self.assertEqual(updated_profile.default_town_or_city, 'Test town')


"""
Profile Order History
"""

class TestOrderHistoryView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser2', password='testpassword2')       

        # Create an order for testing
        self.order = Order.objects.create(
            user_profile=self.user.userprofile, 
            full_name='Test User2',
            email='testuser2@example.com',
            phone_number='1234',
            postcode='BS5',
            town_or_city='Test Town',
            street_address1='123 Test',
            street_address2='Test Road',
            county='Test County',
            date=timezone.now(),
            delivery_cost=5.00,
            order_total=50.00,
            grand_total=55.00,
            original_bag='Test Bag',
            stripe_pid='test_pid'
        )

    def test_order_association_with_profile(self):
        # Fetch the updated UserProfile
        updated_profile = UserProfile.objects.get(user=self.user)
            
        # Verify that the order appears in the user's profile 
        self.assertIn(self.order, updated_profile.orders.all())
